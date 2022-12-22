<h1 align="center">
  <img alt="HTMLarkdown Title" src="https://user-images.githubusercontent.com/35413456/209060922-954f6c6b-8ad9-474d-8901-e03ddc7c4e9c.gif" width="70%">
</h1>

<br>

HTMLarkdown is a HTML-to-Markdown converter that switches to HTML-syntax whenever necessary.

Written completely in **TypeScript**.

<br>

## How is this different?

### Switching to HTML-syntax

Compared to other HTML-to-Markdown converters, HTMLarkdown allows HTML-in

Whenever elements cannot be represented in pure-markdown syntax, HTMLarkdown will switch to HTML-syntax:

```html
<h1>Normal-heading is <strong>boring</strong></h1>
<h1 align="center">
  Centered-heading is <strong>da wae</strong>
</h1>
<p><img alt="My Image" src="https://image.src" /></p>
<p><img alt="My Image" width="80%" src="https://image.src" /></p>
```

```html
# Normal-heading is **boring**

<h1 align="center">
  Centered-heading is <b>da wae</b>
</h1>

![My Image](https://image.src)

<img alt="My Image" width="80%" src="https://image.src" />
```

<br>

HTMLarkdown aims to use as much Markdown-syntax as possible, mixing markdown and HTML if possible:

```html
<blockquote>
  <p align="center">
    Centered-paragraph
  </p>
  <p>Below is a horizontal-rule in blockquote:</p>
  <hr>
</blockquote>
```

```html
> <p align="center">
>   Centered-paragraph
> </p>
> Below is a horizontal-rule in blockquote:
> 
> <hr>
```

<br>

### Edge cases

HTMLarkdown also handles edge cases, such as adding separators to prevent adjacent lists from being combined by markdown-renderers:

```html
<ul>
  <li>List 1 > item 1</li>
  <li>List 1 > item 2</li>
</ul>
<ul>
  <li>List 2 > item 1</li>
  <li>List 2 > item 2</li>
</ul>
```

```
- List 1 > item 1
- List 1 > item 2

<!-- LIST_SEPARATOR -->

- List 2 > item 1
- List 2 > item 2
```
