import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { logout } from '../store/slices/authSlice'
import { clearCart } from '../store/slices/cartSlice'

export const useAuth = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { isAuthenticated, user, profile, loading } = useSelector(state => state.auth)

  const handleLogout = () => {
    dispatch(logout())
    dispatch(clearCart())
    navigate('/login')
  }

  return {
    isAuthenticated,
    user,
    profile,
    loading,
    logout: handleLogout,
  }
}