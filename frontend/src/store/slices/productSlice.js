// src/store/slices/productSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../../services/api'

export const fetchProducts = createAsyncThunk(
  'products/fetchProducts',
  async (params) => {
    const response = await api.get('/products/products/', { params })
    return response.data
  }
)

export const fetchProduct = createAsyncThunk(
  'products/fetchProduct',
  async (slug) => {
    const response = await api.get(`/products/products/${slug}/`)
    return response.data
  }
)

export const fetchFeatured = createAsyncThunk(
  'products/fetchFeatured',
  async () => {
    const response = await api.get('/products/products/featured/')
    return response.data
  }
)

export const fetchNewArrivals = createAsyncThunk(
  'products/fetchNewArrivals',
  async () => {
    const response = await api.get('/products/products/new_arrivals/')
    return response.data
  }
)

export const fetchCategories = createAsyncThunk(
  'products/fetchCategories',
  async () => {
    const response = await api.get('/products/categories/')
    if (response.data.results) {
      return response.data.results
    }
    return response.data
  }
)

const productSlice = createSlice({
  name: 'products',
  initialState: {
    products: [],
    product: null,
    categories: [],
    featured: [],
    newArrivals: [],
    loading: false,
    error: null,
    total_count: 0,
    total_pages: 0,
    current_page: 1,
  },
  reducers: {
    clearProduct: (state) => {
      state.product = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Products
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false
        state.products = action.payload.results || action.payload
        state.total_count = action.payload.count || 0
        state.total_pages = Math.ceil((action.payload.count || 0) / 12)
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      // Fetch Single Product
      .addCase(fetchProduct.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchProduct.fulfilled, (state, action) => {
        state.loading = false
        state.product = action.payload
      })
      // Fetch Featured
      .addCase(fetchFeatured.fulfilled, (state, action) => {
        state.featured = action.payload
      })
      // Fetch New Arrivals
      .addCase(fetchNewArrivals.fulfilled, (state, action) => {
        state.newArrivals = action.payload
      })
      // Fetch Categories
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.categories = action.payload
      })
  },
})

export const { clearProduct } = productSlice.actions
export default productSlice.reducer