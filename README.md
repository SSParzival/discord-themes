# Discord Themes (Modern Discord Compatible)

> Fork of [DEAD1nsane/discord-themes](https://github.com/DEAD1nsane/discord-themes) actualizado y corregido para compatibilidad total con las **últimas versiones de Discord** (Revenge, Bunny, Vendetta, Enmity, Vesktop y Vencord).

---

## 🌟 ¿Qué se corrigió? (Changelog de Compatibilidad)

Anteriormente, los temas de este repositorio fallaban o presentaban errores visuales (botones sin tema, errores de validación, fuentes faltantes o textos ilegibles) en las versiones modernas de Discord. Se aplicaron las siguientes correcciones en cada uno de los 24 temas:

1. **Compatibilidad con el Rediseño Moderno de Discord (React Native v220 - v340+) y Mana UI**:
   - Se corrigió el fallo crítico en Android (`ToastContainer / ManaToastSurface` crash):
     - Incorporación de tokens esenciales: `TOAST_BG`, `ALERT_BG`, `CARD_PRIMARY_BG`, `CARD_PRIMARY_PRESSED_BG`, `CARD_SECONDARY_BG`, `CARD_MUTED_BG`, `MODAL_BACKGROUND`, `MODAL_FOOTER_BACKGROUND`, `BG_SURFACE_OVERLAY`, `BG_SURFACE_OVERLAY_TMP`, `BG_SURFACE_RAISED`, `BG_BASE_PRIMARY`, `BG_BASE_SECONDARY`, `BG_BASE_TERTIARY`, `BG_MOD_FAINT`, `BG_MOD_SUBTLE`, `BG_MOD_STRONG`.
     - Expansión de todos los valores de `semanticColors` a ternas `[dark, light, amoled]`. Esto evita que Discord en modo AMOLED (Midnight) intente acceder al índice 2 y reciba `undefined`, lo que provocaba el crash en el motor de renderizado de React Native.
     - Removido el paquete desactualizado `iconpack: "rosiecord-plumpy"` del bloque `plus` para prevenir fallos en la carga de iconos nativos en Toasts y superficies.
     - Removido el bloque experimental no estándar `sysColors` (Monet) para total conformidad con la especificación `spec: 2`.
   - Soporte exhaustivo para controles de chat y navegación:
     - `CHAT_INPUT_BACKGROUND`, `CHANNELTEXTAREA_BACKGROUND`, `CHAT_INPUT_SEND_BUTTON_ACTIVE_BACKGROUND`, `CHAT_INPUT_ACTION_BUTTON_BACKGROUND`, etc.
     - `CONTROL_PRIMARY_*`, `CONTROL_SECONDARY_*`, `MOBILE_LEGACY_BUTTON_SECONDARY_*` para evitar botones blancos sin tema.
     - `MESSAGE_BACKGROUND_HOVER`, `MESSAGE_MENTIONED_BACKGROUND_DEFAULT`, `MESSAGE_MENTIONED_BACKGROUND_HOVER`, `MENTION_BACKGROUND`, `MENTION_FOREGROUND`.
     - `MESSAGE_AUTOMOD_BACKGROUND_DEFAULT`, `MESSAGE_HIGHLIGHT_BACKGROUND_DEFAULT`.
     - `BACKGROUND_SURFACE_HIGHEST`, `MOBILE_FLOATINGBAR_BACKGROUND`, `MOBILE_HEADER_ICON_DEFAULT`, `NAVIGATOR_HEADER_TINT`.
2. **Actualización de Fuentes (`ggmono-Normal`)**:
   - Discord reemplazó `SourceCodePro-Semibold` por `ggmono-Normal`. Los temas ahora definen `ggmono-Normal` usando la tipografía Gantari, eliminando los errores de paquete de fuentes en los validadores y clientes modernos.
3. **URLs Directas de GitHub**:
   - Se reemplazaron las URLs con redirección (`github.com/.../raw/...`) por enlaces directos sin redirección (`raw.githubusercontent.com/...`), evitando fallos de descarga HTTP 302 en clientes móviles.
4. **Corrección de Errores de Sintaxis y Metadatos**:
   - **`Syn.json`**: Se corrigió el nombre que estaba vacío (`"name": ""`), el cual provocaba error al instalar.
   - **`Rey.json`**: Se corrigió el nombre duplicado `"Syn"` a `"Rey"`.
   - **`PipeBomb.json`**: Se corrigió el color hexadecimal inválido `"PRIMARY_100": "FFFFFFF"` a `"#FFFFFF"`.
   - **Typo**: `BUTTON_OUTLINE_BRAND_BOARDER` fue corregido añadiendo `BUTTON_OUTLINE_BRAND_BORDER` y `BUTTON_OUTLINE_BRAND_BORDER_ACTIVE`.
   - Se movieron tokens semánticos mal ubicados en `rawColors` (`CONTROL_CONNECTED_BACKGROUND_*`) a `semanticColors`.
5. **100% Validado**:
   - Cada uno de los 24 temas pasa la validación oficial del [Revenge / Bunny Theme Validator](https://purple-eyez.github.io/Bunny-Theme-Keys/Validator/) con **0 errores y 0 advertencias**.
6. **Soporte para Escritorio (Vesktop / Vencord / BetterDiscord)**:
   - Se generaron versiones en CSS (`.theme.css`) para cada tema dentro de `Themes/Desktop/` con selectores universales `:root, .theme-dark, .theme-light, .theme-amoled` que combinan variables clásicas (`--background-primary`, `--header-primary`, etc.) y las variables modernas del rediseño (`--bg-base-*`, `--bg-surface-*`, `--text-default`, `--card-*`, `--modal-*`).

---

## 📱 Instalación en Móvil (Revenge / Bunny / Vendetta)

1. **Instala el plugin Themes+** *(Recomendado para iconos personalizados)*:
   - Enlace del plugin: `https://revenge.nexpid.xyz/themes-plus`
   - Configura el modo de Themes+ en **automático**.
2. **Copia el enlace Raw del tema** que desees usar (por ejemplo, de la lista a continuación).
3. En la app de Discord móvil, ve a:
   **Ajustes** ➔ **Revenge** (o **Bunny**) ➔ **Temas** (Themes) ➔ Toca el botón **`+`**.
4. Pega la URL copiada y confirma la instalación.
5. ¡Selecciona el tema y listo!

---

## 💻 Instalación en Escritorio (Vesktop / Vencord / BetterDiscord)

1. Dirígete a la carpeta [`Themes/Desktop/`](./Themes/Desktop/) y abre el archivo `.theme.css` del tema correspondiente.
2. Copia su contenido o su enlace Raw en **Ajustes de Usuario ➔ Vencord / Vesktop ➔ Temas**.

---

## 🎨 Lista de Temas Disponibles

### Temas DARK
| Tema | Descripción | Acento | Enlace Móvil (.json) |
| :--- | :--- | :--- | :--- |
| **Azure Blue AMOLED** | AMOLED black base, usando azul, blanco y gris | `#007FFF` (Azure) | [Ver JSON](./Themes/DARK/Azure%20Blue%20AMOLED.json) |
| **RBW AMOLED** | AMOLED black base, usando rojo, blanco y gris | `#ED0243` (Crimson) | [Ver JSON](./Themes/DARK/RBW%20AMOLED.json) |

### Temas Turbo
| Tema | Descripción | Fondo | Enlace Móvil (.json) |
| :--- | :--- | :--- | :--- |
| **TURBO** | Base AMOLED con rojo, blanco y fondo de volcán | EruptingVolcano | [Ver JSON](./Themes/Turbo/TURBO.json) |
| **Turbo Azure** | Base AMOLED con azul Azure y fondo de volcán | EruptingVolcano | [Ver JSON](./Themes/Turbo/Turbo%20Azure.json) |

### Solicitudes Personalizadas (Custom Requests)
| Tema | Descripción / Acento | Fondo | Enlace Móvil (.json) |
| :--- | :--- | :--- | :--- |
| **Aiharu** | AMOLED con acento Cyan Turquesa (`#55DDEE`) | No | [Ver JSON](./Themes/Custom%20Requests/Aiharu.json) |
| **Bread cat** | AMOLED con acento Gris Pizarra (`#818589`) | No | [Ver JSON](./Themes/Custom%20Requests/Bread%20cat.json) |
| **DRΛGO** | AMOLED con acento Crimson (`#ED0243`) | Sí (`redimg.jpg`) | [Ver JSON](./Themes/Custom%20Requests/DR%CE%9BGO.json) |
| **Iris** | AMOLED con acento Rosa Pastel (`#FFB5FF`) | No | [Ver JSON](./Themes/Custom%20Requests/Iris.json) |
| **Jade** | AMOLED con acento Azul Estético (`#1877F2`) | No | [Ver JSON](./Themes/Custom%20Requests/Jade.json) |
| **Janny (Pinkie Pie)** | AMOLED con acento Azul Celeste (`#7ED0F2`) | No | [Ver JSON](./Themes/Custom%20Requests/Janny.json) |
| **Meow** | AMOLED con acento Púrpura (`#9B26B6`) | Sí (`Meow.jpg`) | [Ver JSON](./Themes/Custom%20Requests/Meow.json) |
| **Niko** | AMOLED con acento Crimson (`#ED0243`) | Sí (`niko.jpg`) | [Ver JSON](./Themes/Custom%20Requests/Niko.json) |
| **PipeBomb** | AMOLED con acento Verde WhatsApp (`#25D366`) | Sí (`WhatsApp.jpg`) | [Ver JSON](./Themes/Custom%20Requests/PipeBomb.json) |
| **Rey** | AMOLED con acento Azul Real (`#0000FF`) | No | [Ver JSON](./Themes/Custom%20Requests/Rey.json) |
| **Super** | AMOLED con acento Rojo Intenso (`#FF0000`) | No | [Ver JSON](./Themes/Custom%20Requests/Super.json) |
| **Syn** | AMOLED con acento Azul Marino (`#000080`) | No | [Ver JSON](./Themes/Custom%20Requests/Syn.json) |
| **Waffle** | AMOLED con acento Amarillo Dorado (`#FFB71B`) | No | [Ver JSON](./Themes/Custom%20Requests/Waffle.json) |
| **broossell** | AMOLED con acento Verde Hoja (`#1FA80D`) | No | [Ver JSON](./Themes/Custom%20Requests/broossell.json) |
| **coffin** | AMOLED con acento Rosa Chicle (`#FF82AD`) | No | [Ver JSON](./Themes/Custom%20Requests/coffin.json) |
| **e.z.o.e** | AMOLED con acento Rojo Puro (`#FF0000`) | No | [Ver JSON](./Themes/Custom%20Requests/e.z.o.e.json) |
| **j.dawggg** | AMOLED con acento Azul Azure (`#007FFF`) | Sí (`j.dawggg.jpg`) | [Ver JSON](./Themes/Custom%20Requests/j.dawggg.json) |
| **n0uzen** | Base Onyx (`#0D0D11`) con Cian (`#0090A3`) y Púrpura (`#9D00FF`) | No | [Ver JSON](./Themes/Custom%20Requests/n0uzen.json) |
| **pessed** | AMOLED con acento Azul Azure (`#007FFF`) | No | [Ver JSON](./Themes/Custom%20Requests/pessed.json) |
| **zephyr** | AMOLED con acento Crimson (`#ED0243`) | Sí (`zephyr.jpg`) | [Ver JSON](./Themes/Custom%20Requests/zephyr.json) |

---

## 🛠️ Herramientas de Desarrollo

En la carpeta [`scripts/`](./scripts/) se encuentra `fix_themes.py`, el cual permite auditar, validar y regenerar los temas CSS a partir de los JSON en cualquier momento:

```bash
python3 scripts/fix_themes.py
```

---

## 🚀 Subir a tu propio repositorio GitHub

Para publicar este fork en tu cuenta de GitHub (`SSParzival/discord-themes`):

```bash
# 1. Crea el repositorio en GitHub (desde la web o con gh repo create SSParzival/discord-themes --public)
# 2. Sube la rama main:
git push -u origin main
```
