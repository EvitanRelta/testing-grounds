import TurndownService from 'turndown'
import TurndownAugmentedNode from './sharedTypes/TurndownAugmentedNode'
import toSanitizedHtmlHOC from './toSanitizedHtmlHOC'

interface AllowedAttr {
    filter: TurndownService.Filter
    allowedAttributes: string[]
}

const turndownHtmlOnly = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced'
})

const allowedAttr: AllowedAttr[] = [
    {
        filter: 'img',
        allowedAttributes: ['src', 'alt', 'width', 'height']
    },
    {
        filter: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'blockquote'],
        allowedAttributes: ['align']
    },
    {
        filter: 'a',
        allowedAttributes: ['href']
    },
    {
        filter: ['br', 'hr', 'em', 'i', 'strong', 'b', 's', 'code'],
        allowedAttributes: []
    }
]

allowedAttr.forEach(
    ({ filter, allowedAttributes }, i) => turndownHtmlOnly.addRule(
        `sanitizedElement${i}`,
        {
            filter,
            replacement: (content, node, options) =>
                toSanitizedHtmlHOC(node as TurndownAugmentedNode, allowedAttributes)(content)
        }
    )
)

turndownHtmlOnly.addRule('htmlCodeblock', {
    filter: 'pre',
    replacement: (content, node, options) =>
        toSanitizedHtmlHOC(node as TurndownAugmentedNode, [], false)(content)
})

export default turndownHtmlOnly