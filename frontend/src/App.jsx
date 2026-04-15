import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import AppRoutes from './AppRoutes'
import Navbar from './components/common/Navbar'
import Footer from './components/common/Footer'
import { fetchCart } from './store/slices/cartSlice'
import { fetchProfile } from './store/slices/authSlice'
import { fetchWishlist } from './store/slices/wishlistSlice'
import { Toaster } from 'react-hot-toast'

function App() {
  const dispatch = useDispatch()
  const token = localStorage.getItem('access_token')

  useEffect(() => {
    if (token) {
      dispatch(fetchProfile())
      dispatch(fetchCart())
      dispatch(fetchWishlist())
    }
  }, [dispatch, token])

  return (
    <>
      <Toaster position="top-right" />
      <Navbar />
      <main className="min-h-screen">
        <AppRoutes />
      </main>
      <Footer />
    </>
  )
}

export default App