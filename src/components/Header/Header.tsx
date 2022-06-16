import { GithubAuthProvider, User } from 'firebase/auth'
import { useState } from 'react'
import MenuButton from './MenuButton'
import ToolbarContainer from './ToolbarContainer'

interface UserStatus {
    loggedIn: boolean
    info: User | null
}

type Props = {
    title: string
    theme: string
    toggleTheme: () => void
    setTitle: React.Dispatch<React.SetStateAction<string>>
    onUpload: (e: React.ChangeEvent<HTMLInputElement>) => void
    lastEditedOn: string
    mdText: string
    setMdText: React.Dispatch<React.SetStateAction<string>>
    onLogin: (provider: GithubAuthProvider) => Promise<void>
    onLogout: () => Promise<void>
    user: UserStatus
}

const Header = ({
    title,
    theme,
    toggleTheme,
    setTitle,
    onUpload,
    lastEditedOn,
    mdText,
    setMdText,
    onLogin,
    onLogout,
    user,
}: Props) => {
    //var for current file name
    const [text, setText] = useState(title)

    //vars for theme control
    const themeColor = theme === 'dark' ? '#181414' : 'white'
    const textColor = theme === 'dark' ? 'white' : '#181414'

    return (
        <header
            style={{
                borderBottom: '1px solid gray',
                marginBottom: '0px',
                padding: '10px',
                paddingBottom: '0px',
                lineHeight: '12px',
            }}
        >
            <div
                style={{
                    justifyContent: 'space-between',
                    display: 'flex',
                }}
            >
                <input
                    type='text'
                    placeholder='Untitled Document'
                    value={text}
                    onChange={(e) => {
                        setText(e.target.value)
                        setTitle(e.target.value)
                    }}
                    style={{
                        border: '0px',
                        fontSize: '25px',
                        width: '30%',
                        backgroundColor: themeColor,
                        color: textColor,
                        marginLeft: 12,
                    }}
                />

                <div>
                    <MenuButton
                        theme={theme}
                        toggleTheme={toggleTheme}
                        title={title}
                        onUpload={onUpload}
                        onLogin={onLogin}
                        onLogout={onLogout}
                        user={user}
                    />
                </div>
            </div>
            <div
                style={{
                    display: 'inline-flex',
                    paddingTop: 5,
                    paddingBottom: 5,
                }}
            >
                <ToolbarContainer
                    onUpload={onUpload}
                    mdText={mdText}
                    title={title}
                    setMdText={setMdText}
                />
                <div
                    style={{
                        color: 'gray',
                        paddingLeft: '5px',
                        marginTop: 5.5,
                        textDecoration: 'underline',
                    }}
                >
                    Last edited on {lastEditedOn}
                </div>
            </div>
        </header>
    )
}

export default Header
