# MindMate Frontend

React-based user interface for the MindMate mental health chatbot.

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Lucide React** - Icon library

## Features

- 🎨 Modern, responsive design
- 😊 Real-time emotion indicators with emojis
- 🎨 Color-coded message bubbles by emotion
- 🚨 Crisis alert styling
- ⚠️ Safety disclaimer modal
- 📱 Mobile-friendly interface
- ♿ Accessibility features

## Development

### Install Dependencies

```bash
npm install
```

### Start Dev Server

```bash
npm run dev
```

Server runs on http://localhost:3000

### Build for Production

```bash
npm run build
```

Output in `dist/` directory

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── main.jsx          # React entry point
├── App.jsx           # Main application component
├── App.css           # Component styles
└── index.css         # Global styles + Tailwind
```

## Configuration

### API Proxy

Backend API is proxied in `vite.config.js`:

```javascript
server: {
  proxy: {
    '/chat': 'http://localhost:8000',
    '/health': 'http://localhost:8000'
  }
}
```

### Styling

Customize theme in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: { /* custom colors */ }
    }
  }
}
```

## Components

### App.jsx

Main component containing:
- **DisclaimerModal** - Safety notice on first visit
- **Header** - App branding and info button
- **ChatContainer** - Message display area
- **InputArea** - Message input and send button

### State Management

```javascript
const [messages, setMessages] = useState([])
const [inputText, setInputText] = useState('')
const [isLoading, setIsLoading] = useState(false)
const [sessionId] = useState(/* unique ID */)
const [showDisclaimer, setShowDisclaimer] = useState(true)
```

### Emotion Styling

```javascript
const EMOTION_COLORS = {
  joy: 'bg-yellow-100 border-yellow-300',
  sadness: 'bg-blue-100 border-blue-300',
  anger: 'bg-red-100 border-red-300',
  // ...
}
```

## API Integration

### Send Message

```javascript
const response = await axios.post('/chat', {
  session_id: sessionId,
  message: inputText
})

// Response: { session_id, emotion, response, crisis }
```

## Customization

### Change Colors

Edit `tailwind.config.js` and `App.jsx` emotion colors.

### Modify Disclaimer

Edit the disclaimer text in `App.jsx` (lines ~70-90).

### Add Features

- User authentication
- Message history export
- Voice input
- Dark mode
- Multi-language support

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast compliance
- Screen reader friendly

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers

## Troubleshooting

**Blank page?**
- Check console for errors
- Verify backend is running
- Clear browser cache

**API errors?**
- Check backend URL in proxy config
- Verify CORS settings in backend
- Check network tab in DevTools

**Styling issues?**
- Run `npm install` again
- Clear Vite cache: `rm -rf node_modules/.vite`
- Rebuild: `npm run build`

## License

MIT License - see [LICENSE](../LICENSE)
