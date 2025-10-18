import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { 
  Send, Heart, AlertTriangle, Info, X, Sparkles, Brain
} from 'lucide-react'
import './App.css'

// Emotion to emoji mapping
const EMOTION_EMOJIS = {
  joy: '😊',
  sadness: '😢',
  anger: '😠',
  fear: '😰',
  love: '❤️',
  surprise: '😲',
  crisis: '🚨',
  neutral: '💭'
}

// Emotion to subtle color mapping (Claude-like)
const EMOTION_COLORS = {
  joy: 'bg-amber-50 border-l-4 border-amber-400',
  sadness: 'bg-blue-50 border-l-4 border-blue-400',
  anger: 'bg-red-50 border-l-4 border-red-400',
  fear: 'bg-purple-50 border-l-4 border-purple-400',
  love: 'bg-pink-50 border-l-4 border-pink-400',
  surprise: 'bg-orange-50 border-l-4 border-orange-400',
  crisis: 'bg-red-100 border-l-4 border-red-600',
  neutral: 'bg-gray-50 border-l-4 border-gray-300'
}

function App() {
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)
  const [showDisclaimer, setShowDisclaimer] = useState(true)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Add welcome message
    setMessages([{
      type: 'bot',
      text: "Hello! I'm MindMate, your AI companion for mental health support. I'm here to listen and provide a safe space for you to share your thoughts and feelings. How are you feeling today?",
      emotion: 'neutral',
      timestamp: new Date()
    }])
  }, [])

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    const userMessage = {
      type: 'user',
      text: inputText,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    try {
      const response = await axios.post('/chat', {
        session_id: sessionId,
        message: inputText
      })

      const botMessage = {
        type: 'bot',
        text: response.data.response,
        emotion: response.data.emotion,
        crisis: response.data.crisis,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        type: 'bot',
        text: "I'm sorry, I'm having trouble responding right now. Please try again in a moment.",
        emotion: 'neutral',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Disclaimer Modal */}
      {showDisclaimer && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-2xl max-w-lg w-full p-8 animate-slide-up border border-gray-200">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center flex-shrink-0">
                <AlertTriangle className="w-6 h-6 text-amber-600" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold text-gray-900 mb-3">Important Notice</h3>
                <div className="text-sm text-gray-700 space-y-3 leading-relaxed">
                  <p>
                    <strong>MindMate is an AI chatbot</strong> designed to provide emotional support and a listening ear.
                  </p>
                  <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                    <p className="text-red-800 font-medium">
                      ⚠️ This is NOT a substitute for professional mental health care.
                    </p>
                  </div>
                  <p className="font-medium text-gray-900">
                    If you're experiencing a mental health crisis or having thoughts of self-harm:
                  </p>
                  <ul className="space-y-2 ml-4">
                    <li className="flex items-start gap-2">
                      <span className="text-blue-600 mt-1">•</span>
                      <span>Call emergency services (112 in India, 911 in US)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-600 mt-1">•</span>
                      <span>Contact AASRA: 91-9820466726 (India, 24/7)</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-blue-600 mt-1">•</span>
                      <span>Reach out to a licensed therapist or counselor</span>
                    </li>
                  </ul>
                  <p className="text-xs text-gray-600 pt-2 border-t border-gray-200">
                    By continuing, you acknowledge that you understand this is an AI tool and not professional therapy.
                  </p>
                </div>
              </div>
            </div>
            <button
              onClick={() => setShowDisclaimer(false)}
              className="w-full bg-gray-900 hover:bg-gray-800 text-white font-medium py-3.5 px-6 rounded-lg transition-colors shadow-sm"
            >
              I Understand, Continue
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="sticky top-0 z-40 bg-white border-b border-gray-200 backdrop-blur-sm bg-opacity-90">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-sm">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">
                MindMate
              </h1>
              <p className="text-xs text-gray-500">AI Mental Health Companion</p>
            </div>
          </div>
          <button
            onClick={() => setShowDisclaimer(true)}
            className="text-gray-400 hover:text-gray-600 transition-colors p-2 hover:bg-gray-100 rounded-lg"
            title="View disclaimer"
          >
            <Info className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Chat Container */}
      <main className="max-w-4xl mx-auto h-[calc(100vh-80px)] flex flex-col">
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto px-6 py-8 space-y-6">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className="animate-fade-in"
              >
                {msg.type === 'user' ? (
                  // User message (Claude-like style)
                  <div className="flex justify-end">
                    <div className="max-w-[85%]">
                      <div className="bg-gray-100 rounded-2xl px-5 py-3.5 shadow-sm">
                        <p className="text-[15px] leading-relaxed text-gray-900 whitespace-pre-wrap">{msg.text}</p>
                      </div>
                      <div className="text-xs text-gray-400 mt-1.5 text-right px-1">
                        {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                ) : (
                  // Bot message (Claude-like style)
                  <div className="flex justify-start">
                    <div className="max-w-[85%] w-full">
                      {/* Emotion indicator (hide love emotion) */}
                      {msg.emotion && msg.emotion !== 'neutral' && msg.emotion !== 'love' && (
                        <div className="flex items-center gap-2 mb-2 px-1">
                          <span className="text-lg">{EMOTION_EMOJIS[msg.emotion]}</span>
                          <span className="text-xs font-medium text-gray-600 capitalize">
                            {msg.emotion === 'crisis' ? 'Crisis Detected' : msg.emotion}
                          </span>
                        </div>
                      )}
                      
                      {/* Message content */}
                      <div
                        className={`rounded-2xl px-5 py-3.5 shadow-sm ${
                          msg.crisis
                            ? 'bg-red-50 border-l-4 border-red-500'
                            : msg.emotion && msg.emotion !== 'neutral'
                            ? EMOTION_COLORS[msg.emotion]
                            : 'bg-white border border-gray-200'
                        }`}
                      >
                        <p className="text-[15px] leading-relaxed text-gray-900 whitespace-pre-wrap">{msg.text}</p>
                      </div>
                      
                      {/* Timestamp */}
                      <div className="text-xs text-gray-400 mt-1.5 px-1">
                        {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
            
            {/* Typing Indicator */}
            {isLoading && (
              <div className="flex justify-start animate-fade-in">
                <div className="bg-white border border-gray-200 rounded-2xl px-5 py-4 shadow-sm">
                  <div className="flex gap-1.5">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area (Claude-like) */}
          <div className="border-t border-gray-200 bg-white px-6 py-4">
            <div className="max-w-3xl mx-auto">
              <div className="flex gap-3 items-end">
                <div className="flex-1 relative">
                  <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Share what's on your mind..."
                    className="w-full resize-none rounded-xl border border-gray-300 px-4 py-3.5 text-[15px] focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-all placeholder:text-gray-400"
                    rows="1"
                    style={{ minHeight: '52px', maxHeight: '200px' }}
                    disabled={isLoading}
                  />
                </div>
                <button
                  onClick={sendMessage}
                  disabled={!inputText.trim() || isLoading}
                  className="bg-gray-900 hover:bg-gray-800 text-white rounded-xl px-5 py-3.5 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-2 font-medium shadow-sm h-[52px]"
                >
                  <Send className="w-4 h-4" />
                  <span className="hidden sm:inline">Send</span>
                </button>
              </div>
              <p className="text-xs text-gray-400 mt-2.5 text-center">
                Press Enter to send • Shift+Enter for new line
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
