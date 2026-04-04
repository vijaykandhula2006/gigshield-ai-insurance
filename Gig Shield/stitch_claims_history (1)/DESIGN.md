# Design System Specification

## 1. Overview & Creative North Star: "The Guardian’s Path"

This design system is engineered to transform complex parametric insurance into a seamless, intuitive journey for the Indian gig economy. We move beyond the "utilitarian app" to create a high-end digital concierge. 

**The Creative North Star: The Guardian’s Path.**
Our aesthetic rejects the cluttered, line-heavy interfaces of traditional finance. Instead, we use **Tonal Layering** and **Editorial Scale** to guide the user. The experience should feel like a series of physical, soft-touch surfaces stacked with intention. By utilizing wide tracking, generous white space, and high-contrast typography, we ensure that even semi-literate users can navigate by "visual weight" and "iconic landmarks" rather than dense reading.

---

## 2. Colors: Depth Over Definition

We utilize a sophisticated Material-based palette. The core principle is **Organic Separation**: we never use lines to separate content; we use light.

### Palette Highlights
- **Primary (`#005440`):** The "Trust Anchor." Used for high-priority actions.
- **Secondary (`#885200`):** The "Incentive Glow." Used for earnings, payouts, and active protection status.
- **Tertiary (`#832c0e`):** The "Critical Alert." Reserved for expired coverage or immediate risks.

### The "No-Line" Rule
Prohibit 1px solid borders for sectioning. Boundaries must be defined solely through background color shifts. A `surface-container-low` (`#f3f3f3`) card must sit on a `surface` (`#f9f9f9`) background to define its edge. 

### The "Glass & Gradient" Rule
For floating elements, like the "File a Claim" FAB or active status indicators, use Glassmorphism:
- **Background:** `primary_container` at 80% opacity.
- **Effect:** 20px Backdrop Blur.
- **Texture:** A subtle linear gradient from `primary` to `primary_container` (Top-Left to Bottom-Right) to give buttons a "gem-like" tactile quality.

---

## 3. Typography: The Editorial Scale

We pair **Plus Jakarta Sans** (Display) with **Inter** (Body) to create an authoritative yet accessible hierarchy.

| Token | Font | Size | Weight | Intent |
| :--- | :--- | :--- | :--- | :--- |
| `display-lg` | Plus Jakarta | 3.5rem | 700 | Large Hero Numbers (e.g., Daily Payout) |
| `headline-md` | Plus Jakarta | 1.75rem | 600 | Clear Section Headers |
| `title-lg` | Inter | 1.375rem | 600 | Card Titles / Primary Actions |
| `body-lg` | Inter | 1.0rem | 400 | Critical Instructional Text |
| `label-md` | Inter | 0.75rem | 500 | Form Labels / Meta-data |

**Visual Logic:** For semi-literate accessibility, use `display-lg` for the "Outcome" (e.g., **₹500**) and `label-md` for the "Context" (e.g., *Rainfall Cover*). The size difference creates a natural focal point that requires no reading to understand the value.

---

## 4. Elevation & Depth: Tonal Layering

Traditional shadows are often "dirty." We use **Ambient Depth** to create a clean, premium atmosphere.

*   **The Layering Principle:** Stack `surface-container-lowest` (#ffffff) cards on top of `surface-container` (#eeeeee) sections. This creates a soft, natural lift.
*   **Ambient Shadows:** For floating modals, use a custom shadow: 
    *   `box-shadow: 0px 12px 32px rgba(26, 28, 28, 0.06);`
    *   This uses the `on-surface` color at a very low opacity for a natural, diffused look.
*   **The Ghost Border:** If a container is placed on a white background, use the `outline-variant` token at **15% opacity** as a "Ghost Border" to softly contain the content without adding visual noise.

---

## 5. Components: Tactile & High-Contrast

All components use a standard `md` (12px) or `lg` (16px) corner radius to feel friendly and modern.

### Buttons
- **Primary:** High-contrast `primary` background with `on-primary` text. Always use `surface-tint` for subtle top-down gradients to make the button feel "clickable."
- **Secondary:** `secondary_container` background with `on-secondary_container` text. Used for "Add-on" services or non-critical actions.

### Data Cards & Lists
- **Forbid Dividers:** Use `Spacing Scale 3` (1rem) or background shifts (`surface-container-low` vs `surface-container-high`) to separate items.
- **Visual Anchors:** Every list item must have a leading `primary_fixed` icon container (circular or `xl` roundedness) to allow users to scan by icon shape and color.

### Input Fields
- Avoid "Box" inputs. Use a "Minimalist Tray" approach: a `surface-container-highest` background with a `none` border and a thick 2px `primary` bottom-border that activates on focus.

### The "Status Ring" (Custom Component)
For parametric triggers (e.g., rain intensity or accident alerts), use a concentric ring component using `secondary` and `secondary_fixed` to show "active protection" status. This provides an immediate "Trust Signal" on the home screen.

---

## 6. Do’s and Don'ts

### Do
- **Do** prioritize large icons over long text labels.
- **Do** use `Spacing Scale 5` (1.7rem) for gutters to give the UI "breathing room" typical of high-end fintech like CRED.
- **Do** use `tertiary` (#832c0e) sparingly—only when the user is at risk of losing coverage.

### Don’t
- **Don’t** use pure black (#000000). Always use `on-surface` (#1a1c1c) for text to maintain a softer, premium contrast.
- **Don’t** use 1px dividers between list items. It makes the app feel "cheap" and dated.
- **Don’t** use standard Material shadows. Always use the diffused Ambient Shadows defined in Section 4.