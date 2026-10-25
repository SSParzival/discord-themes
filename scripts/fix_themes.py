import os
import sys
import json
import glob
import re

U = [
    'ABCGintoNord-ExtraBold', 'ggsans-Bold', 'ggsans-BoldItalic', 'ggsans-ExtraBold',
    'ggsans-ExtraBoldItalic', 'ggsans-Medium', 'ggsans-MediumItalic', 'ggsans-Normal',
    'ggsans-NormalItalic', 'ggsans-Semibold', 'ggsans-SemiboldItalic', 'NotoSans-Bold',
    'NotoSans-ExtraBold', 'NotoSans-Medium', 'NotoSans-Normal', 'NotoSans-NormalItalic',
    'NotoSans-Semibold', 'ggmono-Normal'
]

def is_hex(e):
    return bool(re.match(r'^#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{8}|[0-9A-Fa-f]{3}|[0-9A-Fa-f]{4})$', e))

def is_rgba(e):
    m = re.match(r'^rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(0|1|0?\.\d+|1\.0)\s*\)$', e, re.I)
    if not m:
        return False
    parts = [float(p) for p in m.groups()]
    return 0 <= parts[0] <= 255 and 0 <= parts[1] <= 255 and 0 <= parts[2] <= 255 and 0 <= parts[3] <= 1

def is_valid_color(e):
    return isinstance(e, str) and (is_hex(e) or is_rgba(e) or e == 'transparent')

def validate_theme(d):
    errors = []
    warnings = []
    if not isinstance(d.get('name'), str) or not d.get('name').strip():
        errors.append('"name" must be non-empty string')
    if not isinstance(d.get('description'), str) or not d.get('description').strip():
        errors.append('"description" must be non-empty string')
    if d.get('spec') != 2:
        errors.append(f'"spec" must be equal to 2 (got {d.get("spec")})')
    if not isinstance(d.get('authors'), list):
        errors.append('"authors" must be list')
    else:
        for i, a in enumerate(d['authors']):
            if not isinstance(a.get('name'), str):
                errors.append(f'author {i} invalid name')
    
    if 'semanticColors' in d:
        if not isinstance(d['semanticColors'], dict):
            errors.append('semanticColors must be dict')
        else:
            for k, v in d['semanticColors'].items():
                if not isinstance(v, list):
                    errors.append(f'semanticColors[{k}] must be list')
                elif len(v) < 3:
                    errors.append(f'semanticColors[{k}] must have at least 3 elements (got {len(v)})')
                else:
                    for c in v:
                        if not is_valid_color(c):
                            errors.append(f'semanticColors[{k}] invalid color: {c}')
    
    if 'rawColors' in d:
        if not isinstance(d['rawColors'], dict):
            errors.append('rawColors must be dict')
        else:
            for k, v in d['rawColors'].items():
                if isinstance(v, list):
                    errors.append(f'rawColors[{k}] cannot be list')
                elif not is_valid_color(v):
                    errors.append(f'rawColors[{k}] invalid color: {v}')
                    
    if 'fonts' in d:
        if not isinstance(d['fonts'], dict):
            errors.append('fonts must be dict')
        else:
            for req in U:
                if req not in d['fonts']:
                    errors.append(f'Missing font: {req}')
                        
    if 'plus' in d:
        if d['plus'].get('version') != 0:
            errors.append('plus.version must be 0')
            
    return errors, warnings

def to_triple(val):
    if isinstance(val, str):
        return [val, val, val]
    if isinstance(val, list):
        if len(val) >= 3:
            return val[:3]
        if len(val) == 2:
            return [val[0], val[1], val[0]]
        if len(val) == 1:
            return [val[0], val[0], val[0]]
    return ['#000000', '#000000', '#000000']

def process_themes(repo_dir, check_only=False):
    desktop_dir = os.path.join(repo_dir, 'Themes', 'Desktop')
    scripts_dir = os.path.join(repo_dir, 'scripts')

    if not check_only:
        os.makedirs(desktop_dir, exist_ok=True)
        os.makedirs(scripts_dir, exist_ok=True)

    files = sorted(glob.glob(os.path.join(repo_dir, 'Themes', '**', '*.json'), recursive=True))
    print(f'Processing {len(files)} themes (check_only={check_only})...')

    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            d = json.load(fp)
            
        # Metadata name fixes
        if f.endswith('Syn.json') and not d.get('name'):
            d['name'] = 'Syn'
        elif f.endswith('Rey.json') and d.get('name') == 'Syn':
            d['name'] = 'Rey'
            
        # PipeBomb PRIMARY_100
        if f.endswith('PipeBomb.json') and d.get('rawColors', {}).get('PRIMARY_100') == 'FFFFFFF':
            d['rawColors']['PRIMARY_100'] = '#FFFFFF'
            
        # Fonts: point to SSParzival/discord-themes fork
        fonts = d.setdefault('fonts', {})
        for k, v in list(fonts.items()):
            v_clean = v.replace('https://github.com/DEAD1nsane/discord-themes/raw/refs/heads/main/', 'https://raw.githubusercontent.com/SSParzival/discord-themes/main/')
            v_clean = v_clean.replace('https://raw.githubusercontent.com/DEAD1nsane/discord-themes/main/', 'https://raw.githubusercontent.com/SSParzival/discord-themes/main/')
            v_clean = v_clean.replace('?raw=1', '')
            fonts[k] = v_clean
        fonts['ggmono-Normal'] = 'https://raw.githubusercontent.com/SSParzival/discord-themes/main/Fonts/Gantari-Semibold.ttf'
        fonts['SourceCodePro-Semibold'] = 'https://raw.githubusercontent.com/SSParzival/discord-themes/main/Fonts/Gantari-Semibold.ttf'
        
        # Background: point to SSParzival/discord-themes fork
        if 'background' in d and 'url' in d['background']:
            bg_url = d['background']['url']
            bg_url = bg_url.replace('/refs/heads/main/', '/main/')
            bg_url = bg_url.replace('https://raw.githubusercontent.com/DEAD1nsane/discord-themes/main/', 'https://raw.githubusercontent.com/SSParzival/discord-themes/main/')
            bg_url = bg_url.replace('https://github.com/DEAD1nsane/discord-themes/raw/main/', 'https://raw.githubusercontent.com/SSParzival/discord-themes/main/')
            d['background']['url'] = bg_url
            
        # Clean up Themes+ to avoid crashes from discontinued/incompatible rosiecord iconpack
        if 'plus' in d:
            if 'iconpack' in d['plus']:
                del d['plus']['iconpack']
                
        # Remove legacy non-spec sysColors block
        if 'sysColors' in d:
            del d['sysColors']
            
        sem = d.setdefault('semanticColors', {})
        raw = d.setdefault('rawColors', {})
        
        # Misplaced raw tokens
        for token in ['CONTROL_CONNECTED_BACKGROUND_ACTIVE', 'CONTROL_CONNECTED_BACKGROUND_DEFAULT']:
            if token in raw:
                val = raw.pop(token)
                if token not in sem:
                    sem[token] = [val]
                    
        # Typo fix
        if 'BUTTON_OUTLINE_BRAND_BOARDER' in sem:
            b_val = sem['BUTTON_OUTLINE_BRAND_BOARDER']
            sem.setdefault('BUTTON_OUTLINE_BRAND_BORDER', b_val)
            sem.setdefault('BUTTON_OUTLINE_BRAND_BORDER_ACTIVE', b_val)
            
        # Base colors extraction
        is_amoled_theme = 'amoled' in d.get('name', '').lower() or 'amoled' in f.lower()
        bg_base_val = '#000000' if is_amoled_theme else (sem.get('BACKGROUND_BASE_LOW', ['#000000'])[0])
        bg_base = to_triple(bg_base_val)
        
        brand_color = sem.get('BACKGROUND_BRAND', sem.get('TEXT_LINK', ['#ED0243' if is_amoled_theme else '#007FFF']))
        brand_color_3 = to_triple(brand_color)
        
        text_strong_val = sem.get('TEXT_STRONG', sem.get('MOBILE_TEXT_HEADING_PRIMARY', ['#FFFFFF']))[0]
        text_strong = to_triple(text_strong_val)
        
        text_default_val = sem.get('TEXT_DEFAULT', ['#FFFFFF' if is_amoled_theme else '#DBDEE1'])[0]
        text_default = to_triple(text_default_val)
        
        text_muted_val = sem.get('TEXT_MUTED', [brand_color_3[0] if is_amoled_theme else '#949BA4'])[0]
        text_muted = to_triple(text_muted_val)
        
        text_link_val = sem.get('TEXT_LINK', brand_color_3)[0]
        text_link = to_triple(text_link_val)
        
        # Chat Input
        if 'REDESIGN_CHAT_INPUT_BACKGROUND' in sem:
            sem.setdefault('CHAT_INPUT_BACKGROUND', sem['REDESIGN_CHAT_INPUT_BACKGROUND'])
        sem.setdefault('CHAT_INPUT_BACKGROUND', bg_base)
        sem.setdefault('CHANNELTEXTAREA_BACKGROUND', sem['CHAT_INPUT_BACKGROUND'])
        sem.setdefault('CHAT_INPUT_ACTION_BUTTON_BACKGROUND', to_triple('#00000000'))
        sem.setdefault('CHAT_INPUT_ACTION_BUTTON_ICON_DEFAULT_TINT', sem.get('INTERACTIVE_ICON_DEFAULT', text_muted))
        sem.setdefault('CHAT_INPUT_ACTION_ICON_ACTIVE_TINT', sem.get('INTERACTIVE_ICON_ACTIVE', brand_color_3))
        sem.setdefault('CHAT_INPUT_SEND_BUTTON_ACTIVE_BACKGROUND', brand_color_3)
        sem.setdefault('CHAT_INPUT_SEND_BUTTON_ICON_ACTIVE_TINT', to_triple('#FFFFFF'))
        
        # Legacy button styles
        if 'REDESIGN_BUTTON_SECONDARY_BACKGROUND' in sem:
            sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_BACKGROUND_DEFAULT', sem['REDESIGN_BUTTON_SECONDARY_BACKGROUND'])
        if 'REDESIGN_BUTTON_SECONDARY_BORDER' in sem:
            sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_BORDER_DEFAULT', sem['REDESIGN_BUTTON_SECONDARY_BORDER'])
        sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_BACKGROUND_DEFAULT', bg_base)
        sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_BORDER_DEFAULT', bg_base)
        sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_TEXT_DEFAULT', text_default)
        
        # Modern controls
        sem.setdefault('CONTROL_PRIMARY_BACKGROUND_DEFAULT', brand_color_3)
        sem.setdefault('CONTROL_PRIMARY_BACKGROUND_ACTIVE', sem.get('REDESIGN_BUTTON_PRIMARY_PRESSED_BACKGROUND', brand_color_3))
        sem.setdefault('CONTROL_PRIMARY_BORDER_DEFAULT', to_triple('#00000000'))
        sem.setdefault('CONTROL_PRIMARY_BORDER_ACTIVE', to_triple('#00000000'))
        sem.setdefault('CONTROL_PRIMARY_TEXT_DEFAULT', text_strong)
        sem.setdefault('CONTROL_SECONDARY_BACKGROUND_DEFAULT', sem.get('REDESIGN_BUTTON_SECONDARY_BACKGROUND', bg_base))
        sem.setdefault('CONTROL_SECONDARY_BACKGROUND_ACTIVE', sem.get('REDESIGN_BUTTON_PRIMARY_PRESSED_BACKGROUND', bg_base))
        sem.setdefault('CONTROL_SECONDARY_BORDER_DEFAULT', sem.get('REDESIGN_BUTTON_SECONDARY_BORDER', bg_base))
        sem.setdefault('CONTROL_SECONDARY_BORDER_ACTIVE', brand_color_3)
        sem.setdefault('CONTROL_SECONDARY_TEXT_DEFAULT', text_default)
        
        # Dangerous border
        if 'BUTTON_OUTLINE_DANGER_BORDER' in sem:
            d_val = sem['BUTTON_OUTLINE_DANGER_BORDER']
            sem.setdefault('CONTROL_CRITICAL_PRIMARY_BORDER_DEFAULT', d_val)
            sem.setdefault('CONTROL_CRITICAL_PRIMARY_BORDER_ACTIVE', d_val)
            
        # Automod, Highlight, Mentions
        if 'BACKGROUND_MESSAGE_AUTOMOD' in sem:
            sem.setdefault('MESSAGE_AUTOMOD_BACKGROUND_DEFAULT', sem['BACKGROUND_MESSAGE_AUTOMOD'])
        if 'BACKGROUND_MESSAGE_AUTOMOD_HOVER' in sem:
            sem.setdefault('MESSAGE_AUTOMOD_BACKGROUND_HOVER', sem['BACKGROUND_MESSAGE_AUTOMOD_HOVER'])
        if 'BACKGROUND_MESSAGE_HIGHLIGHT' in sem:
            sem.setdefault('MESSAGE_HIGHLIGHT_BACKGROUND_DEFAULT', sem['BACKGROUND_MESSAGE_HIGHLIGHT'])
        if 'BACKGROUND_MESSAGE_HIGHLIGHT_HOVER' in sem:
            sem.setdefault('MESSAGE_HIGHLIGHT_BACKGROUND_HOVER', sem['BACKGROUND_MESSAGE_HIGHLIGHT_HOVER'])
        if 'BACKGROUND_MENTIONED' in sem:
            sem.setdefault('MESSAGE_MENTIONED_BACKGROUND_DEFAULT', sem['BACKGROUND_MENTIONED'])
            sem.setdefault('MENTION_BACKGROUND', sem['BACKGROUND_MENTIONED'])
        if 'BACKGROUND_MENTIONED_HOVER' in sem:
            sem.setdefault('MESSAGE_MENTIONED_BACKGROUND_HOVER', sem['BACKGROUND_MENTIONED_HOVER'])
        sem.setdefault('MENTION_FOREGROUND', sem.get('TEXT_LINK', brand_color_3))
        
        # Core standard Discord background tokens
        sem.setdefault('BACKGROUND_PRIMARY', bg_base)
        sem.setdefault('BACKGROUND_SECONDARY', bg_base)
        sem.setdefault('BACKGROUND_SECONDARY_ALT', bg_base)
        sem.setdefault('BACKGROUND_TERTIARY', bg_base)
        sem.setdefault('BACKGROUND_ACCENT', sem.get('BACKGROUND_ACCENT', to_triple('#08080830' if is_amoled_theme else '#1E1F22')))
        sem.setdefault('BACKGROUND_FLOATING', bg_base)
        sem.setdefault('BACKGROUND_MOBILE_PRIMARY', bg_base)
        sem.setdefault('BACKGROUND_MOBILE_SECONDARY', bg_base)
        sem.setdefault('CHAT_BACKGROUND', bg_base)
        
        # Surfaces, Header, Navigation
        sem.setdefault('BACKGROUND_BASE_LOW', bg_base)
        sem.setdefault('BACKGROUND_BASE_LOWER', bg_base)
        sem.setdefault('BACKGROUND_BASE_LOWEST', bg_base)
        sem.setdefault('BACKGROUND_SURFACE_HIGH', bg_base)
        sem.setdefault('BACKGROUND_SURFACE_HIGHEST', bg_base)
        sem.setdefault('BG_SURFACE_OVERLAY', bg_base)
        sem.setdefault('BG_SURFACE_OVERLAY_TMP', bg_base)
        sem.setdefault('BG_SURFACE_RAISED', bg_base)
        sem.setdefault('BG_BASE_PRIMARY', bg_base)
        sem.setdefault('BG_BASE_SECONDARY', bg_base)
        sem.setdefault('BG_BASE_TERTIARY', bg_base)
        sem.setdefault('BG_MOD_FAINT', sem['BACKGROUND_ACCENT'])
        sem.setdefault('BG_MOD_SUBTLE', sem['BACKGROUND_ACCENT'])
        sem.setdefault('BG_MOD_NORMAL', bg_base)
        sem.setdefault('BG_MOD_STRONG', bg_base)
        
        # CRITICAL Mana & Toast tokens (prevents ManaToastSurface / ToastContainer crash)
        sem.setdefault('TOAST_BG', bg_base)
        sem.setdefault('ALERT_BG', bg_base)
        sem.setdefault('MODAL_BACKGROUND', bg_base)
        sem.setdefault('MODAL_FOOTER_BACKGROUND', bg_base)
        sem.setdefault('CARD_PRIMARY_BG', bg_base)
        sem.setdefault('CARD_PRIMARY_PRESSED_BG', to_triple('#1A1A1A' if is_amoled_theme else '#2B2D31'))
        sem.setdefault('CARD_SECONDARY_BG', bg_base)
        sem.setdefault('CARD_MUTED_BG', bg_base)
        sem.setdefault('CARD_MUTED_PRESSED_BG', bg_base)
        sem.setdefault('STATUS_WARNING_BACKGROUND', to_triple('#F0B232'))
        sem.setdefault('STATUS_DANGER_BACKGROUND', to_triple('#F23F43'))
        sem.setdefault('STATUS_POSITIVE_BACKGROUND', to_triple('#23A55A'))
        
        # Standard Text & Interactive tokens
        sem.setdefault('HEADER_PRIMARY', text_strong)
        sem.setdefault('HEADER_SECONDARY', text_muted)
        sem.setdefault('TEXT_NORMAL', text_default)
        sem.setdefault('TEXT_DEFAULT', text_default)
        sem.setdefault('TEXT_STRONG', text_strong)
        sem.setdefault('TEXT_MUTED', text_muted)
        sem.setdefault('TEXT_LINK', text_link)
        sem.setdefault('INTERACTIVE_NORMAL', sem.get('INTERACTIVE_ICON_DEFAULT', text_muted))
        sem.setdefault('INTERACTIVE_HOVER', sem.get('INTERACTIVE_ICON_HOVER', text_default))
        sem.setdefault('INTERACTIVE_ACTIVE', sem.get('INTERACTIVE_ICON_ACTIVE', brand_color_3))
        sem.setdefault('INTERACTIVE_MUTED', sem.get('INTERACTIVE_MUTED', to_triple('#2A2A2A')))
        
        # Mobile specific elements
        sem.setdefault('MOBILE_FLOATINGBAR_BACKGROUND', bg_base)
        sem.setdefault('MOBILE_FLOATINGBAR_BACKGROUND_HIGHER', bg_base)
        sem.setdefault('MOBILE_FLOATING_ACCESSORY_BACKGROUND', bg_base)
        sem.setdefault('MOBILE_HEADER_ICON_DEFAULT', sem.get('INTERACTIVE_ICON_DEFAULT', text_muted))
        sem.setdefault('MOBILE_HEADER_ICON_ACTIVE', sem.get('INTERACTIVE_ICON_ACTIVE', brand_color_3))
        sem.setdefault('NAVIGATOR_HEADER_TINT', bg_base)
        sem.setdefault('MOBILE_HEADER_BORDER', sem.get('BORDER_SUBTLE', to_triple('#FFFFFF0A')))
        sem.setdefault('TEXT_SUBTLE', text_muted)
        
        # Ensure EVERY semanticColors entry has 3 elements [dark, light, amoled]
        # This prevents undefined lookups when Discord is in AMOLED mode (themeIndex = 2)
        for k, v in list(sem.items()):
            sem[k] = to_triple(v)
            
        # Validate
        errs, warns = validate_theme(d)
        if errs or warns:
            raise ValueError(f'Validation failed for {f}: {errs}, {warns}')

        if check_only:
            continue

        # Write back JSON
        with open(f, 'w', encoding='utf-8') as fp:
            json.dump(d, fp, indent=2, ensure_ascii=False)
            fp.write('\n')
            
        # Desktop CSS version
        theme_name = d['name']
        theme_desc = d.get('description', '')
        safe_name = os.path.basename(f).replace('.json', '.theme.css')
        css_path = os.path.join(desktop_dir, safe_name)
        
        bg_color = bg_base[0]
        txt_color = text_default[0]
        strong_color = text_strong[0]
        muted_color = text_muted[0]
        accent_color = brand_color_3[0]
        link_color = text_link[0]
        bg_accent_color = sem['BACKGROUND_ACCENT'][0]
        chat_input_bg = sem['CHAT_INPUT_BACKGROUND'][0]
        
        bg_css = ''
        if 'background' in d and 'url' in d['background']:
            bg_url = d['background']['url']
            bg_alpha = float(d['background'].get('alpha', 0.3))
            bg_css = f"""
#app-mount {{
  background: linear-gradient(rgba(0, 0, 0, {1.0 - bg_alpha:.2f}), rgba(0, 0, 0, {1.0 - bg_alpha:.2f})), url('{bg_url}') center/cover no-repeat fixed !important;
}}
"""
        
        css_content = f"""/**
 * @name {theme_name}
 * @author {d.get('authors', [{}])[0].get('name', 'im__turbo__')}
 * @version 1.0.0
 * @description {theme_desc}
 * @source https://github.com/SSParzival/discord-themes
*/

:root, .theme-dark, .theme-light, .theme-amoled {{
  /* Legacy Discord CSS variables */
  --background-primary: {bg_color} !important;
  --background-secondary: {bg_color} !important;
  --background-secondary-alt: {bg_color} !important;
  --background-tertiary: {bg_color} !important;
  --background-accent: {bg_accent_color} !important;
  --background-floating: {bg_color} !important;
  --channeltextarea-background: {chat_input_bg} !important;
  --chat-background: {bg_color} !important;

  --header-primary: {strong_color} !important;
  --header-secondary: {muted_color} !important;
  --text-normal: {txt_color} !important;
  --text-muted: {muted_color} !important;
  --text-link: {link_color} !important;

  --interactive-normal: {sem['INTERACTIVE_NORMAL'][0]} !important;
  --interactive-hover: {sem['INTERACTIVE_HOVER'][0]} !important;
  --interactive-active: {sem['INTERACTIVE_ACTIVE'][0]} !important;
  --interactive-muted: {sem['INTERACTIVE_MUTED'][0]} !important;
  --brand-experiment: {accent_color} !important;
  --brand-experiment-500: {accent_color} !important;
  --brand-experiment-560: {accent_color} !important;
  --button-secondary-background: {bg_color} !important;
  --button-secondary-border: {bg_color} !important;

  --background-mentioned: {sem.get('MESSAGE_MENTIONED_BACKGROUND_DEFAULT', [accent_color + '40'])[0]} !important;
  --background-mentioned-hover: {sem.get('MESSAGE_MENTIONED_BACKGROUND_HOVER', [accent_color + '40'])[0]} !important;
  --background-message-hover: {sem.get('MESSAGE_BACKGROUND_HOVER', [bg_color])[0]} !important;

  /* Modern Discord (Redesign / New CSS variables) */
  --bg-base-primary: {bg_color} !important;
  --bg-base-secondary: {bg_color} !important;
  --bg-base-tertiary: {bg_color} !important;
  --bg-surface-raised: {bg_color} !important;
  --bg-surface-overlay: {bg_color} !important;
  --bg-mod-faint: {bg_accent_color} !important;
  --bg-mod-subtle: {bg_accent_color} !important;
  --bg-mod-normal: {bg_color} !important;
  --bg-mod-strong: {bg_color} !important;

  --text-default: {txt_color} !important;
  --text-strong: {strong_color} !important;
  --text-subtle: {muted_color} !important;
  --interactive-default: {sem['INTERACTIVE_NORMAL'][0]} !important;

  --input-background: {chat_input_bg} !important;
  --modal-background: {bg_color} !important;
  --modal-footer-background: {bg_color} !important;
  --card-primary-bg: {bg_color} !important;
  --card-secondary-bg: {bg_color} !important;
  --card-muted-bg: {bg_color} !important;
}}
{bg_css}
"""
        with open(css_path, 'w', encoding='utf-8') as cfp:
            cfp.write(css_content)

    print(f'Successfully processed, validated, and generated CSS for all {len(files)} themes!')

if __name__ == '__main__':
    repo_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(os.path.join(repo_directory, 'Themes')):
        repo_directory = '/home/ssparzival/Proyectos/GitHub/discord-themes'
    is_check = '--check' in sys.argv
    process_themes(repo_directory, check_only=is_check)
