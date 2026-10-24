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
                    if req == 'ggmono-Normal' and 'SourceCodePro-Semibold' in d['fonts']:
                        warnings.append('SourceCodePro-Semibold replaced by ggmono-Normal')
                    else:
                        errors.append(f'Missing font: {req}')
                        
    if 'plus' in d:
        if d['plus'].get('version') != 0:
            errors.append('plus.version must be 0')
            
    return errors, warnings

repo_dir = '/home/ssparzival/Proyectos/GitHub/discord-themes'
desktop_dir = os.path.join(repo_dir, 'Themes', 'Desktop')
scripts_dir = os.path.join(repo_dir, 'scripts')
os.makedirs(desktop_dir, exist_ok=True)
os.makedirs(scripts_dir, exist_ok=True)

files = sorted(glob.glob(os.path.join(repo_dir, 'Themes', '**', '*.json'), recursive=True))
print(f'Processing {len(files)} themes...')

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
        
    # Fonts
    fonts = d.setdefault('fonts', {})
    for k, v in list(fonts.items()):
        v_clean = v.replace('https://github.com/DEAD1nsane/discord-themes/raw/refs/heads/main/', 'https://raw.githubusercontent.com/DEAD1nsane/discord-themes/main/')
        v_clean = v_clean.replace('?raw=1', '')
        fonts[k] = v_clean
    fonts['ggmono-Normal'] = 'https://raw.githubusercontent.com/DEAD1nsane/discord-themes/main/Fonts/Gantari-Semibold.ttf'
    fonts['SourceCodePro-Semibold'] = 'https://raw.githubusercontent.com/DEAD1nsane/discord-themes/main/Fonts/Gantari-Semibold.ttf'
    
    # Background
    if 'background' in d and 'url' in d['background']:
        bg_url = d['background']['url']
        d['background']['url'] = bg_url.replace('/refs/heads/main/', '/main/')
        
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
        
    # Chat Input
    if 'REDESIGN_CHAT_INPUT_BACKGROUND' in sem:
        sem.setdefault('CHAT_INPUT_BACKGROUND', sem['REDESIGN_CHAT_INPUT_BACKGROUND'])
    sem.setdefault('CHAT_INPUT_ACTION_BUTTON_BACKGROUND', ['#00000000'])
    sem.setdefault('CHAT_INPUT_ACTION_BUTTON_ICON_DEFAULT_TINT', sem.get('INTERACTIVE_ICON_DEFAULT', sem.get('TEXT_MUTED', ['#FFFFFF'])))
    sem.setdefault('CHAT_INPUT_ACTION_ICON_ACTIVE_TINT', sem.get('INTERACTIVE_ICON_ACTIVE', sem.get('TEXT_LINK', ['#007FFF'])))
    brand_color = sem.get('BACKGROUND_BRAND', sem.get('TEXT_LINK', ['#007FFF']))
    sem.setdefault('CHAT_INPUT_SEND_BUTTON_ACTIVE_BACKGROUND', brand_color)
    sem.setdefault('CHAT_INPUT_SEND_BUTTON_ICON_ACTIVE_TINT', ['#FFFFFF'])
    
    # Legacy button styles
    if 'REDESIGN_BUTTON_SECONDARY_BACKGROUND' in sem:
        sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_BACKGROUND_DEFAULT', sem['REDESIGN_BUTTON_SECONDARY_BACKGROUND'])
    if 'REDESIGN_BUTTON_SECONDARY_BORDER' in sem:
        sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_BORDER_DEFAULT', sem['REDESIGN_BUTTON_SECONDARY_BORDER'])
    sem.setdefault('MOBILE_LEGACY_BUTTON_SECONDARY_TEXT_DEFAULT', sem.get('TEXT_DEFAULT', ['#FFFFFF']))
    
    # Modern controls
    sem.setdefault('CONTROL_PRIMARY_BACKGROUND_DEFAULT', brand_color)
    sem.setdefault('CONTROL_PRIMARY_BACKGROUND_ACTIVE', sem.get('REDESIGN_BUTTON_PRIMARY_PRESSED_BACKGROUND', brand_color))
    sem.setdefault('CONTROL_PRIMARY_BORDER_DEFAULT', ['#00000000'])
    sem.setdefault('CONTROL_PRIMARY_BORDER_ACTIVE', ['#00000000'])
    sem.setdefault('CONTROL_PRIMARY_TEXT_DEFAULT', sem.get('TEXT_STRONG', ['#FFFFFF']))
    sem.setdefault('CONTROL_SECONDARY_BACKGROUND_DEFAULT', sem.get('REDESIGN_BUTTON_SECONDARY_BACKGROUND', ['#000000']))
    sem.setdefault('CONTROL_SECONDARY_BACKGROUND_ACTIVE', sem.get('REDESIGN_BUTTON_PRIMARY_PRESSED_BACKGROUND', ['#000000']))
    sem.setdefault('CONTROL_SECONDARY_BORDER_DEFAULT', sem.get('REDESIGN_BUTTON_SECONDARY_BORDER', ['#000000']))
    sem.setdefault('CONTROL_SECONDARY_BORDER_ACTIVE', brand_color)
    sem.setdefault('CONTROL_SECONDARY_TEXT_DEFAULT', sem.get('TEXT_DEFAULT', ['#FFFFFF']))
    
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
    sem.setdefault('MENTION_FOREGROUND', sem.get('TEXT_LINK', brand_color))
    
    # Surfaces & Header
    bg_base = sem.get('BACKGROUND_BASE_LOW', ['#000000'])
    sem.setdefault('BACKGROUND_SURFACE_HIGHEST', bg_base)
    sem.setdefault('MOBILE_FLOATINGBAR_BACKGROUND', bg_base)
    sem.setdefault('MOBILE_FLOATINGBAR_BACKGROUND_HIGHER', bg_base)
    sem.setdefault('MOBILE_FLOATING_ACCESSORY_BACKGROUND', bg_base)
    sem.setdefault('MOBILE_HEADER_ICON_DEFAULT', sem.get('INTERACTIVE_ICON_DEFAULT', ['#FFFFFF']))
    sem.setdefault('NAVIGATOR_HEADER_TINT', bg_base)
    sem.setdefault('MOBILE_HEADER_BORDER', sem.get('BORDER_SUBTLE', ['#FFFFFF0A']))
    sem.setdefault('TEXT_SUBTLE', sem.get('TEXT_MUTED', ['#818589']))
    
    # Validate
    errs, warns = validate_theme(d)
    if errs or warns:
        raise ValueError(f'Validation failed for {f}: {errs}, {warns}')
        
    # Write back
    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(d, fp, indent=2, ensure_ascii=False)
        fp.write('\n')
        
    # Desktop CSS version
    theme_name = d['name']
    theme_desc = d.get('description', '')
    safe_name = os.path.basename(f).replace('.json', '.theme.css')
    css_path = os.path.join(desktop_dir, safe_name)
    
    bg_color = bg_base[0]
    txt_color = sem.get('TEXT_DEFAULT', ['#FFFFFF'])[0]
    muted_color = sem.get('TEXT_MUTED', ['#818589'])[0]
    accent_color = brand_color[0]
    link_color = sem.get('TEXT_LINK', brand_color)[0]
    
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

:root {{
  /* Backgrounds */
  --background-primary: {bg_color} !important;
  --background-secondary: {bg_color} !important;
  --background-secondary-alt: {bg_color} !important;
  --background-tertiary: {bg_color} !important;
  --background-accent: {sem.get('BACKGROUND_ACCENT', ['#08080830'])[0]} !important;
  --background-floating: {bg_color} !important;
  --channeltextarea-background: {sem.get('CHAT_INPUT_BACKGROUND', [bg_color])[0]} !important;
  --chat-background: {bg_color} !important;

  /* Text & Headers */
  --header-primary: {sem.get('MOBILE_TEXT_HEADING_PRIMARY', ['#FFFFFF'])[0]} !important;
  --header-secondary: {muted_color} !important;
  --text-normal: {txt_color} !important;
  --text-muted: {muted_color} !important;
  --text-link: {link_color} !important;

  /* Interactive & Accents */
  --interactive-normal: {sem.get('INTERACTIVE_ICON_DEFAULT', [muted_color])[0]} !important;
  --interactive-hover: {sem.get('INTERACTIVE_ICON_HOVER', [txt_color])[0]} !important;
  --interactive-active: {sem.get('INTERACTIVE_ICON_ACTIVE', [accent_color])[0]} !important;
  --interactive-muted: {sem.get('INTERACTIVE_MUTED', ['#2A2A2A'])[0]} !important;
  --brand-experiment: {accent_color} !important;
  --brand-experiment-500: {accent_color} !important;
  --brand-experiment-560: {accent_color} !important;
  --button-secondary-background: {sem.get('MOBILE_LEGACY_BUTTON_SECONDARY_BACKGROUND_DEFAULT', [bg_color])[0]} !important;
  --button-secondary-border: {sem.get('MOBILE_LEGACY_BUTTON_SECONDARY_BORDER_DEFAULT', [bg_color])[0]} !important;

  /* Mentions & Hover */
  --background-mentioned: {sem.get('MESSAGE_MENTIONED_BACKGROUND_DEFAULT', [accent_color + '40'])[0]} !important;
  --background-mentioned-hover: {sem.get('MESSAGE_MENTIONED_BACKGROUND_HOVER', [accent_color + '40'])[0]} !important;
  --background-message-hover: {sem.get('MESSAGE_BACKGROUND_HOVER', [bg_color])[0]} !important;
}}
{bg_css}
"""
    with open(css_path, 'w', encoding='utf-8') as cfp:
        cfp.write(css_content)

print(f'Successfully processed, validated, and generated CSS for all {len(files)} themes!')
