<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/EvitanRelta/testing-grounds/master/assets/htmlarkdown_dark_bigger_text.webp">
    <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/35413456/209442374-03df7a77-bfd9-4329-85d7-2d89f18ddc2a.png">
    <img alt="HTMLarkdown Title" src="https://raw.githubusercontent.com/EvitanRelta/testing-grounds/master/assets/htmlarkdown_dark_bigger_text.webp" width="90%">
  </picture>
</h1>

<br>

HTMLarkdown is a **<ins>HTML-to-Markdown converter</ins>** that's able to output HTML-syntax when required.  
Like for center-aligning:

```html
# Heading Markdown

<h1 align="center">
  Centered Heading (needs to be in HTML-syntax)
</h1>
```

Written completely in <img height="15" src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Typescript_logo_2020.svg"> **<ins>TypeScript</ins>**.

<br>

# How is this different?

## Switching to HTML-syntax

Whenever elements **<ins>cannot be represented in markdown-syntax**</ins>, HTMLarkdown will **<ins>switch to HTML-syntax</ins>**:

<table>
    <thead>
        <tr>
            <th width=500>Input HTML</th>
            <th width=500>Output Markdown</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
<pre lang="html"><code>&lt;h1>Normal-heading is &lt;strong>boring&lt;/strong>&lt;/h1>
<!-- BLANK_LINE -->
&lt;h1 align="center">
  Centered-heading is &lt;strong>da wae&lt;/strong>
&lt;/h1>
<!-- BLANK_LINE -->
&lt;p>&lt;img src="https://image.src" />&lt;/p>
<!-- BLANK_LINE -->
&lt;p>&lt;img width="80%" src="https://image.src" />&lt;/p>
</code></pre>
            </td>
            <td>
<pre lang="html"><code># Normal-heading is **boring**
<!-- BLANK_LINE -->
&lt;h1 align="center">
  Centered-heading is &lt;b>da wae&lt;/b>
&lt;/h1>
<!-- BLANK_LINE -->
![](https://image.src)
<!-- BLANK_LINE -->
&lt;img width="80%" src="https://image.src" />
</code></pre>
            </td>
        </tr>
    </tbody>
</table>


<br>

But HTMLarkdown tries use as **<ins>little HTML-syntax</ins>** as possible. **<ins>Mixing markdown and HTML</ins>** if needed:

<table>
    <thead>
        <tr>
            <th width=500>Input HTML</th>
            <th width=500>Output Markdown</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
<pre lang="html"><code>&lt;blockquote>
  &lt;p align="center">
    Centered-paragraph
  &lt;/p>
  &lt;p>Below is a horizontal-rule in blockquote:&lt;/p>
  &lt;hr>
&lt;/blockquote>
</code></pre>
            </td>
            <td>
<pre lang="html"><code>> &lt;p align="center">
>   Centered-paragraph
> &lt;/p>
> Below is a horizontal-rule in blockquote:
> 
> &lt;hr>
</code></pre>
            </td>
        </tr>
    </tbody>
</table>
