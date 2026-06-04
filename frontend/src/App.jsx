import { useEffect, useState } from 'react'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [path, setPath] = useState(window.location.pathname)
  const [token, setToken] = useState(localStorage.getItem('token') || '')

  useEffect(() => {
    const onPopState = () => setPath(window.location.pathname)
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  }, [])

  const navigate = (nextPath) => {
    if (window.location.pathname !== nextPath) {
      window.history.pushState({}, '', nextPath)
      setPath(nextPath)
    }
  }

  useEffect(() => {
    if (token && path === '/') {
      navigate('/dashboard')
    }
    if (!token && path === '/dashboard') {
      navigate('/')
    }
  }, [token, path])

  if (path === '/dashboard') {
    return (
      <DashboardPage
        token={token}
        onLogout={() => {
          localStorage.removeItem('token')
          setToken('')
          navigate('/')
        }}
        onUnauthorized={() => {
          localStorage.removeItem('token')
          setToken('')
          navigate('/')
        }}
      />
    )
  }

  return (
    <AuthPage
      onSuccess={(nextToken) => {
        localStorage.setItem('token', nextToken)
        setToken(nextToken)
        navigate('/dashboard')
      }}
    />
  )
}

function AuthPage({ onSuccess }) {
  const [mode, setMode] = useState('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await fetch(`${API_BASE}/auth/${mode}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Request failed')
      }

      onSuccess(data.token)
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page-shell">
      <section className="box auth-box">
        <h1>Trading Dashboard</h1>
        <div className="tabs">
          <button type="button" onClick={() => setMode('login')} className={mode === 'login' ? 'active' : ''}>
            Login
          </button>
          <button type="button" onClick={() => setMode('register')} className={mode === 'register' ? 'active' : ''}>
            Register
          </button>
        </div>
        <form onSubmit={submit} className="stack">
          <label>
            Username
            <input value={username} onChange={(event) => setUsername(event.target.value)} />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? 'Working...' : mode === 'login' ? 'Login' : 'Register'}
          </button>
        </form>
        {message ? <p className="message">{message}</p> : null}
      </section>
    </main>
  )
}

function DashboardPage({ token, onLogout, onUnauthorized }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')
  const [quantities, setQuantities] = useState({})

  useEffect(() => {
    const loadDashboard = async () => {
      setLoading(true)
      setMessage('')

      try {
        const response = await fetch(`${API_BASE}/portfolio/dashboard`, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        const payload = await response.json()
        if (!response.ok) {
          if (response.status === 401) {
            onUnauthorized()
            return
          }
          throw new Error(payload.detail || 'Dashboard request failed')
        }

        setData(payload)
      } catch (error) {
        setMessage(error.message)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [token, onUnauthorized])

  const submitTrade = async (symbol, endpoint) => {
    const quantity = Number(quantities[symbol] || 1)
    setMessage('')

    try {
      const response = await fetch(`${API_BASE}/trades/${endpoint}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol, quantity }),
      })

      const payload = await response.json()
      if (!response.ok) {
        if (response.status === 401) {
          onUnauthorized()
          return
        }
        throw new Error(payload.detail || 'Trade failed')
      }

      setData(payload)
    } catch (error) {
      setMessage(error.message)
    }
  }

  if (loading) {
    return <main className="page-shell"><section className="box">Loading...</section></main>
  }

  if (!data) {
    return <main className="page-shell"><section className="box">No data loaded.</section></main>
  }

  return (
    <main className="page-shell dashboard-shell">
      <header className="box header-box">
        <div>
          <h1>Dashboard</h1>
          <p>User: {data.username}</p>
          <p>Balance: {data.balance}</p>
        </div>
        <button type="button" onClick={onLogout}>Logout</button>
      </header>

      <section className="box">
        <h2>Stocks</h2>
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Price</th>
              <th>Qty</th>
              <th>Buy</th>
              <th>Sell</th>
            </tr>
          </thead>
          <tbody>
            {data.stocks.map((stock) => (
              <tr key={stock.id}>
                <td>{stock.symbol}</td>
                <td>{stock.name}</td>
                <td>{stock.current_price}</td>
                <td>
                  <input
                    type="number"
                    min="1"
                    value={quantities[stock.symbol] || 1}
                    onChange={(event) =>
                      setQuantities((current) => ({ ...current, [stock.symbol]: event.target.value }))
                    }
                  />
                </td>
                <td><button type="button" onClick={() => submitTrade(stock.symbol, 'buy')}>Buy</button></td>
                <td><button type="button" onClick={() => submitTrade(stock.symbol, 'sell')}>Sell</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="box">
        <h2>Holdings</h2>
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {data.holdings.length ? (
              data.holdings.map((holding) => (
                <tr key={holding.id}>
                  <td>{holding.symbol}</td>
                  <td>{holding.name}</td>
                  <td>{holding.quantity}</td>
                  <td>{holding.current_price}</td>
                  <td>{holding.value}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">No holdings yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>

      <section className="box">
        <h2>Transactions</h2>
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Type</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {data.transactions.length ? (
              data.transactions.map((transaction) => (
                <tr key={transaction.id}>
                  <td>{transaction.symbol}</td>
                  <td>{transaction.type}</td>
                  <td>{transaction.quantity}</td>
                  <td>{transaction.price}</td>
                  <td>{new Date(transaction.timestamp).toLocaleString()}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">No transactions yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>

      {message ? <section className="box message">{message}</section> : null}
    </main>
  )
}

export default App
