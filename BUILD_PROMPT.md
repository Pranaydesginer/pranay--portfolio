# Build Prompt: Pranay Chowdary Puthumbaka, Product Design Portfolio

> Paste this whole prompt into Claude Code (opened inside the `pranay-portfolio` folder), or into a new chat in the "Pranay's Portfolio" Project. It describes everything built so far, so the site can be continued or recreated exactly.

---

## 1. Your role and how to work with me

Act as my Senior Product Designer, UI/UX mentor, frontend developer and technical guide. I'm a Product Designer and a beginner at coding.

- Explain any new concept simply, say why it's needed, tell me exactly what to click or type, give commands one at a time, describe the expected result, and wait for my confirmation before the next major step.
- Treat the design described here as approved. Don't redesign, add visual elements, or change copy without asking me.
- Never invent metrics, research findings or results. Use only facts I give you.
- Never use copyrighted characters, props or artwork (e.g. Marvel's Infinity Gauntlet) or copy other designers' illustrations or copy. All visuals must be original.
- Keep code clean, commented and consistent. After every change, check desktop, mobile, light mode and dark mode.

---

## 2. Tech stack and folder structure

- **Plain HTML, CSS and JavaScript.** No frameworks, no build step, no npm packages.
- Font: **Inter** from Google Fonts (weights 300, 400, 500, 600, 700), with fallbacks `"Segoe UI", system-ui, -apple-system, sans-serif`.
- Version control: **Git + GitHub**. Hosting: **Vercel Hobby (free)**. Open `index.html` directly to preview.

```
pranay-portfolio/
├── index.html              Home page (built)
├── about.html              About page (next)
├── projects.html           Projects page (later)
├── assets/
│   ├── css/styles.css      All styles and design tokens
│   ├── js/main.js          Welcome screen, intro, theme, sound
│   ├── images/             pranay-about-photo.jpg, project images
│   └── files/resume.pdf    Resume
├── CLAUDE.md               Full project brief
├── BUILD_PROMPT.md         This file
└── README.md
```

Every page shares the same `<head>` (fonts, stylesheet, theme-init script), the same navigation and the same footer. Keep them identical across pages.

---

## 3. Design tokens (CSS variables in `:root`)

| Token | Light | Dark |
|---|---|---|
| `--bg` page background | `#FAFAFA` | `#111111` |
| `--surface` nav pill / cards | `#F2F2F2` | `#1A1A1A` |
| `--surface-2` chips / buttons / windows | `#FFFFFF` | `#1E1E1E` |
| `--text` body text (charcoal) | `#333333` | `#E6E6E6` |
| `--text-strong` headings / bold | `#1F1F1F` | `#F5F5F5` |
| `--muted` secondary text | `#6E6E6E` | `#9A9A9A` |
| `--line` borders, frame lines | `#E3E3E3` | `#262626` |
| `--line-dot` frame dots, intro lines | `#CFCFCF` | `#3A3A3A` |
| `--pill` / `--pill-border` | `#F0F0F0` / `#D9D9D9` | `#1C1C1C` / `#333333` |
| `--btn` / `--btn-text` primary button | `#2A2A2A` / `#FFFFFF` | `#F2F2F2` / `#141414` |
| `--accent` (tiny touches only) | `#E5383B` | `#FF5A5F` |
| Hand skin `--skin-1/2/3` | `#F0D0B2` / `#E4B791` / `#D3A07A` | same |
| Hand outline / creases | `#8A573A` / `#9C6544` | same |
| Sleeve `--sleeve-1/2` | `#3A3A3A` / `#262626` | `#4A4A4A` / `#333333` |

Other values: `--maxw: 1240px`, radius 10–14px for buttons and chips, `--ease: cubic-bezier(.2,.7,.2,1)`. Focus ring: 2px solid accent, 3px offset.

**Style rules:** calm and clean. The page stays neutral, with colour coming only from the hand illustration and project images. Headlines mix **light (300)** and **bold (700)** weights. Meta lines use small round dots as separators.

---

## 4. Theme (light / dark)

- An inline script in `<head>` runs before the page paints. It reads `localStorage['pp-theme']`, and if nothing is saved it follows `prefers-color-scheme`. It sets `data-theme="light|dark"` on `<html>`.
- The theme button in the nav toggles the theme and saves the choice to `localStorage['pp-theme']`. It shows a moon icon in light mode and a sun icon in dark mode.
- Wrap every `localStorage`/`sessionStorage` call in try/catch.

---

## 5. Sound

- **Off by default.** The state is saved in `localStorage['pp-sound']` (`on` / `off`).
- Toggles: a speaker icon button in the nav, and a "SOUND OFF / SOUND ON" pill at the bottom of the welcome screen. Both stay in sync. When off, the speaker's wave line drops to 15% opacity.
- Sounds are generated with the Web Audio API, with no audio files: a short sine "click" (gain ramps 0.0001 → 0.08 → 0.0001 over about 120 ms). Frequencies: Enter 520 Hz, theme 440 Hz, sound toggle 660 Hz, each greeting 380 + 40×index Hz, Welcome 700 Hz.

---

## 6. Welcome screen (shown once per visit)

- A full-screen fixed overlay (`z-index: 50`) with background `--bg`, with its content centred.
- A small **browser-window card**, 230px wide: a top bar with three small grey dots, and a body where the word **"Welcome"** types in letter by letter (140 ms per letter), followed by a blinking accent-coloured caret.
- An **Enter ↵** button in dark (`--btn`), with an enter-arrow icon.
- The hint "PRESS ENTER OR CLICK TO CONTINUE" in small uppercase muted text with letter-spacing.
- The sound pill at the bottom centre.
- **Enter, Space or a click** continues. Afterwards it sets `sessionStorage['pp-welcomed']`, so it doesn't appear again in the same visit. It fades out over 0.5 s, then the intro transition plays.

---

## 7. Intro transition (plays after Enter)

A full-screen overlay (`z-index: 49`) with background `--bg`. The centre cell is `min(440px, 76vw)` wide and `150px` tall (`120px` on mobile).

**Timeline:**
1. **0.06 s:** four thin 1px lines in `--line-dot` draw out from the centre (horizontal lines scale X from 0 to 1; vertical lines scale Y from 0 to 1, with a 0.15 s delay, over 0.7 s). Together they frame the centre cell as part of a 3×3 grid.
2. Corner labels fade in (0.4 s delay), in 10.5px uppercase muted text with letter-spacing, sitting just outside each corner of the cell:
   - top-left **PRANAY CHOWDARY**, top-right **PRODUCT DESIGNER**
   - bottom-left **DESIGNING WITH AI**, bottom-right **PORTFOLIO · 2026**
   - Hidden on mobile.
3. **From 0.7 s:** greetings cycle in the cell every **380 ms**: **Hello → नमस्ते → నమస్కారం → Hola → Bonjour → Ciao**. They're 40–64px bold. Each swap blurs and fades out, then in (about 160–180 ms).
4. **About 3.2 s:** an accent-red block wipes in from the left over the cell (scaleX 0 → 1, 0.45 s), showing **"Welcome."** in white bold.
5. **About 4.2 s:** the block fades out.
6. **About 4.5 s:** the lines shrink away, the overlay fades out, and the Home page content reveals.

- A **Skip** button at the bottom right, plus **Esc or Enter**, ends the intro immediately.
- With `prefers-reduced-motion: reduce`, the intro is skipped entirely.

---

## 8. Navigation (all pages)

- Sticky at the top, with a semi-transparent `--bg` background (85%), a 10px backdrop blur and a 1px bottom border.
- **Left:** the logo "Pranay**.**", where the dot is in the accent colour. It links to `index.html`.
- **Centre:** a pill-shaped group (on `--surface`, with a border and 4px padding) containing **Home · About · Projects**. The active item has a white raised background and a **small accent dot** at its top-right.
- **Right:** the sound icon button, the theme icon button (38×38, bordered) and a dark **Resume ↗** button linking to `assets/files/resume.pdf` in a new tab.
- **Mobile (≤640px):** the links move to a full-width row below, and the Resume button shows only its icon.

---

## 9. Home page: hero

Content sits in a centred frame (`max-width: 1240px`) with **thin 1px vertical lines on the left and right** and a **bottom line with small dots** at the corners, in Neelesh-style structure lines.

The hero has **two columns** (1.05fr / 1fr), padding `88px 56px 96px`, and a minimum height of the viewport minus the nav.

**Left column, in order:**
1. **Status pill:** a green dot with a soft glow, then "Currently Product Designer at Cixcent Technologies"
2. "Hi, I'm **Pranay Chowdary Puthumbaka** 👋" in 18px muted text, with the name bold
3. **Headline**, `clamp(38px, 4.6vw, 60px)`, weight 300, tight letter-spacing:
   "I turn **complex workflows** into **simple, human** experiences." (bold parts at 700)
4. **Description**, 17px muted, max 540px wide:
   "Product Designer designing B2B SaaS, ERP and fintech products. I specialise in mapping user flows and turning complex business workflows into user-centred, easy-to-use designs, from requirement gathering to high-fidelity UI."
5. **Meta line:** Product Designer • B2B SaaS & ERP • Hyderabad, India
6. **Buttons:** **View projects →** (dark, links to `projects.html`) and **About me** (outlined, links to `about.html`). On hover they lift 2px and gain a soft shadow.

**Right column:** a 3-column layout of [skill chips] [hand] [skill chips].
- **Left chips:** Product Design · User Research · Interaction Design · Wireframing
- **Right chips:** Prototyping · Visual Design · AI-Centered Design · User-Centered Design
- Chips are white with a 1px border, 10px radius and 13.5px medium text. Every second chip is offset 16px outward, which gives a staggered look.
- **Hand:** an original inline SVG, 230px wide, with a soft accent-tinted radial glow behind it and a slow **float** animation (±8px, 6 s loop). Its SVG source is in `index.html` and should be kept as is: a natural open palm with a skin gradient, palm-cup shading, finger highlights, knuckle and palm creases, an outline and a dark shirt cuff.

**Load reveal:** after the intro, the pill, greeting, headline, description, meta, buttons and visual fade up 14px in a stagger (0.05–0.45 s delays).

**Responsive:**
- At **≤1020px**, the hero becomes a single column with the visual centred below the text.
- At **≤640px**, the hand appears above the chips, and the chips wrap in centred rows without offsets.

---

## 10. Footer (all pages)

One row, wrapping on mobile: "© 2026 Pranay Chowdary Puthumbaka", then **pranaydesigner03@gmail.com** · **LinkedIn ↗** · **Behance ↗** in 14px muted text.
- LinkedIn: https://www.linkedin.com/in/pranay-chowdary-puthumbaka-728284301/
- Behance: https://www.behance.net/pranayputhumb

---

## 11. Accessibility checklist

- Use semantic landmarks (`header`, `nav`, `main`, `section`, `footer`), with `aria-current="page"` on the active nav link.
- Every icon button has an `aria-label`. Sound toggles use `aria-pressed`.
- Show a visible focus ring on everything that can be clicked or tabbed to.
- The welcome screen and intro can be used with the keyboard alone (Enter, Space, Esc).
- Respect `prefers-reduced-motion`.
- Keep text contrast at least 4.5:1 in both themes.

---

## 12. What comes next (don't build until I confirm)

1. **About page (`about.html`):** who I am, with my photo (`assets/images/pranay-about-photo.jpg`, cropped waist-up, door number cropped out, background softened slightly); design philosophy; design process (Research → Ideate → Design → Test → Iterate); an experience timeline (Cixcent Technologies, Product Designer, Feb 2026 – Present, with the line "Also worked on Loans 24K, a retailer loan management web app"; Beetsl Soft Solutions, virtual internship, Aug 2025 – Jan 2026); education (B.Tech ECE, Bharat Institute of Higher Education & Research, 2021–2025); skills and tools; a resume download; an **FAQ accordion**; and a **contact section** (email, LinkedIn, Behance, phone only if approved, and a contact form).
2. **Projects page (`projects.html`):** project cards (an outcome-sentence title, description, a real-facts line, mockups, a tag). Clicking the card opens the on-site case study; a "View on Behance ↗" button opens Behance. I'll supply the project screens.
3. Then deploy to **Vercel** from GitHub.

See `CLAUDE.md` for the full project brief, FAQ answers and project list.
