import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../../services/api'

export const login = createAsyncThunk('auth/login', async ({ username, password }) => {
  const response = await api.post('/auth/login/', { username, password })
  localStorage.setItem('access_token', response.data.access)
  localStorage.setItem('refresh_token', response.data.refresh)
  return response.data
})

export const register = createAsyncThunk('auth/register', async (userData) => {
  const response = await api.post('/auth/register/', userData)
  return response.data
})

export const fetchProfile = createAsyncThunk('auth/fetchProfile', async () => {
  const response = await api.get('/auth/profile/')
  return response.data
})

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    profile: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      state.user = null
      state.profile = null
      state.isAuthenticated = false
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isAuthenticated = true
        state.loading = false
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      .addCase(fetchProfile.fulfilled, (state, action) => {
        state.profile = action.payload
        state.user = action.payload.user
        state.isAuthenticated = true
      })
      .addCase(register.pending, (state) => {
        state.loading = true
      })
      .addCase(register.fulfilled, (state, action) => {
        state.loading = false
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
  },
})

export const { logout } = authSlice.actions
export default authSlice.reducer