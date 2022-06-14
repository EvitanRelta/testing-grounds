import FormatAlignLeftIcon from '@mui/icons-material/FormatAlignLeft'
import { Menu, MenuItem } from '@mui/material'
import IconButton from '@mui/material/IconButton'
import { useState } from 'react'
import textAlign from './toolbarFunctions/textAlign'

// interface Props {
//     editor: Editor | null;
// }

export default ({ editor }) => {
    const onChange = (alignment) => {
        textAlign(editor)(alignment)
    }
    const [anchor, setAnchor] = useState(null)

    const openMenu = (e) => {
        setAnchor(e.currentTarget)
    }

    const closeMenu = () => {
        setAnchor(null)
    }

    const alignOptions = ['left', 'center', 'right', 'justify']

    const capitaliseFirstLetter = (string) => {
        return string.charAt(0).toUpperCase() + string.substring(1)
    }

    return (
        <div style={{ display: 'inline' }}>
            <IconButton onClick={openMenu}>
                <FormatAlignLeftIcon />
            </IconButton>
            <Menu
                open={Boolean(anchor)}
                keepMounted
                anchorEl={anchor}
                onClose={closeMenu}
            >
                {alignOptions.map((option, index) => (
                    <MenuItem key={index} onClick={() => onChange(option)}>
                        {capitaliseFirstLetter(option)}
                    </MenuItem>
                ))}
            </Menu>
            {/* <select value='' onChange={onChange}>
                <option hidden>Alignment</option>
                <option value='left'>Left</option>
                <option value='center'>Center</option>
                <option value='right'>Right</option>
                <option value='justify'>Justify</option>
            </select> */}
        </div>
    )
}
