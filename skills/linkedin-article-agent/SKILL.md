---
name: linkedin-article-agent
description: Create engaging LinkedIn articles with proper formatting, emojis, clickable links, and code blocks. Use for technical tutorials, LinkedIn article formatting, adding visual appeal with emojis, structuring content with headings and lists, and including hashtags with resource links. Always adds #createdbyzai hashtag.
---

# LinkedIn Article Agent

## Overview

Create engaging, properly formatted LinkedIn articles with visual appeal, emojis, clickable links, and code blocks. This skill leverages Playwright to interact directly with LinkedIn's article editor.

## Quick Start

1. Navigate to LinkedIn
2. Click "Write article"
3. Follow formatting workflow below
4. Always include `#createdbyzai` hashtag at the end
5. **Optional:** Schedule article for later using scheduling workflow below

## Article Structure Workflow

### Step 1: Title and Hook

Add a compelling headline and opening hook:

```
🎯 We've all been there.
You push a seemingly harmless change to production...
```

**Pattern:**
- Start with emoji + bold statement
- 2-3 short paragraphs (1-2 sentences each)
- Build emotional connection with common pain point
- End with transition to solution

### Step 2: Section Format

Use this pattern for each major section:

```javascript
// Horizontal rule separator
insertHR();

// Section heading with emoji + bold
insertP("⚠️ <strong>THE PROBLEM WITH CSS SELECTORS</strong>");

// Content paragraph with links
insertP("When I started with <a href='https://playwright.dev'>Playwright</a>...");

// Bullet list with emojis
insertList([
  "✏️ First point",
  "🎨 Second point",
  "❌ Third point"
]);
```

### Step 3: Code Blocks

Format code examples with proper indentation:

```javascript
insertCode(`<!-- ❌ Bad: Tied to CSS -->
<button className="btn-primary">Submit</button>

<!-- ✅ Good: Decoupled from implementation -->
<button className="btn-primary" data-testid="login-submit-button">
  Submit
</button>`);
```

**Best practices:**
- Use 4-space indentation
- Include comments with emojis (❌ ✅)
- Keep examples concise but complete
- Show both bad and good patterns when relevant

### Step 4: Links and Resources

Add clickable links throughout:

```javascript
insertP("📚 <strong>RESOURCES</strong>");
insertList([
  "🔗 <a href='https://playwright.dev'>Playwright Documentation</a>",
  "🔗 <a href='https://react.dev'>React Documentation</a>"
]);
```

### Step 5: Closing and Hashtags

**Required: Always include #createdbyzai hashtag**

```javascript
insertP("💬 <em>Have questions? Drop a comment below!</em>");
insertP("🎉 <strong>Happy testing!</strong> 🚀");
insertP("");
insertP("#react #playwright #testing #webdev #typescript #createdbyzai");
```

## Formatting Patterns

### Emojis by Section Type

| Section | Emojis |
|---------|--------|
| Hook | 🎯 💥 😱 |
| Problem | ⚠️ 🚫 📌 |
| Solution | ✨ 🎯 💡 |
| Setup | 🚀 📦 ⚙️ 📚 |
| Code | 🎨 🎯 🔖 |
| Testing | ✅ ▶️ 🎮 |
| Automation | 🤖 📊 |
| Best Practices | 💡 ✅ ❌ |
| Takeaways | 🎓 1️⃣2️⃣3️⃣ |
| Resources | 📚 🔗 |
| Closing | 💬 🎉 🙏 |

### Text Formatting

- **Bold headings**: `<strong>HEADING TEXT</strong>`
- **Emphasis**: Wrap key phrases in `<strong>`
- **Inline code**: `<code>code snippet</code>`
- **Links**: `<a href='url'>link text</a>`
- **Italic**: `<em>text</em>`

### Section Separators

Always use `<hr>` between major sections:

```javascript
const insertHR = () => {
  const hr = document.createElement('hr');
  editor.appendChild(hr);
};
```

## LinkedIn Editor Helper Functions

Use these functions when building articles:

```javascript
// Paragraph with HTML
const insertP = (text) => {
  const p = document.createElement('p');
  p.innerHTML = text;
  editor.appendChild(p);
};

// Code block
const insertCode = (code) => {
  const pre = document.createElement('pre');
  const codeEl = document.createElement('code');
  codeEl.textContent = code;
  pre.appendChild(codeEl);
  editor.appendChild(pre);
};

// Bullet list
const insertList = (items) => {
  const ul = document.createElement('ul');
  items.forEach(item => {
    const li = document.createElement('li');
    const p = document.createElement('p');
    p.innerHTML = item;
    li.appendChild(p);
    ul.appendChild(li);
  });
  editor.appendChild(ul);
};
```

## Content Guidelines

### DO:

✅ Use short paragraphs (1-2 sentences)
✅ Add emojis liberally but purposefully
✅ Include horizontal rules between sections
✅ Add clickable links to resources
✅ Use bold text for headings and emphasis
✅ Include code examples with syntax
✅ End with `#createdbyzai` hashtag

### DON'T:

❌ Write long dense paragraphs
❌ Overuse emojis (keep it professional)
❌ Use markdown syntax (LinkedIn doesn't render it)
❌ Forget section separators
❌ Skip the closing call-to-action

## Article Templates

### Technical Tutorial Structure

1. **Hook** - Common pain point
2. **Problem** - What goes wrong
3. **Solution** - Your approach
4. **Setup** - Installation/steps
5. **Implementation** - Code examples
6. **Best Practices** - DO's and DON'Ts
7. **Takeaways** - Numbered list
8. **Resources** - Clickable links
9. **CTA + Hashtags** (include `#createdbyzai`)

## Common Tasks

### Creating a New Article

```javascript
// Clear editor
editor.innerHTML = '<p></p>';
editor.focus();

// Build article section by section
insertP("🎯 <strong>We've all been there.</strong>");
insertP("Your hook here...");
insertHR();
// Continue with sections...
```

### Adding Links

```javascript
// External link
insertP("Check out <a href='https://example.com'>this resource</a>");

// Multiple links in list
insertList([
  "🔗 <a href='url1'>Link 1</a>",
  "🔗 <a href='url2'>Link 2</a>"
]);
```

### Formatting Code

```javascript
insertCode(`// Your code here
function example() {
  return true;
}`);
```

### Scheduling an Article for Later

After completing the article, you may want to schedule it for a specific date/time:

```javascript
// Step 1: Click Next to open publish modal
const nextButton = document.querySelector('button[aria-label="Next"]');
if (nextButton) nextButton.click();

// Step 2: Add post content (optional promotional text)
const postContentArea = document.querySelector('div.ql-editor');
if (postContentArea) {
  postContentArea.click();
  postContentArea.textContent = 'Your promotional post content here...';
}

// Step 3: Click the Schedule post button
const scheduleButton = document.querySelector('button[aria-label="Schedule post"]');
if (scheduleButton) scheduleButton.click();

// Step 4: Select date from calendar
const dayButtons = document.querySelectorAll('button[data-daynum]');
const targetDay = Array.from(dayButtons).find(btn =>
  btn.getAttribute('data-daynum') === '10' // Use target day number
);
if (targetDay) {
  targetDay.scrollIntoView({ block: 'center' });
  targetDay.click();
}

// Step 5: Set the time
const timeInput = document.querySelector('input[aria-label="Time"]');
if (timeInput) {
  timeInput.value = '9:00 AM'; // Set desired time
  timeInput.dispatchEvent(new Event('input', { bubbles: true }));
  timeInput.dispatchEvent(new Event('change', { bubbles: true }));
}

// Step 6: Click Next to confirm date/time
const confirmNextButton = document.querySelector('button[aria-label="Next"]');
if (confirmNextButton && !confirmNextButton.hasAttribute('disabled')) {
  confirmNextButton.click();
}

// Step 7: Click Schedule to finalize
const scheduleFinalButton = Array.from(document.querySelectorAll('button'))
  .find(btn => btn.textContent.trim() === 'Schedule');
if (scheduleFinalButton) scheduleFinalButton.click();

// Step 8: Close confirmation dialog
const closeButton = Array.from(document.querySelectorAll('button'))
  .find(btn => btn.textContent.trim() === 'Close');
if (closeButton) closeButton.click();
```

**Important notes for scheduling:**
- Use `button[data-daynum="XX"]` selector to find calendar days (XX = day number 1-31)
- The time input uses 12-hour format with AM/PM (e.g., "9:00 AM", "3:30 PM")
- Check if Next button is disabled before clicking (`hasAttribute('disabled')`)
- Calendar day buttons may need `scrollIntoView()` before clicking if not visible
- Wait for UI updates between steps using `setTimeout()` or Playwright's built-in waits

## Resources

### references/emoji-cheat-sheet.md

Comprehensive emoji guide organized by section type, including:
- Section-heading emojis (hook, problem, solution, etc.)
- Status emojis (success, error, progress)
- Tech-specific emojis (languages, frameworks, tools)
- Formatting tips and best practices

Load this reference when selecting emojis for article sections to maintain consistent visual appeal.
