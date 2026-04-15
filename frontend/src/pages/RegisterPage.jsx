import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../store/slices/authSlice'
import toast from 'react-hot-toast'

const RegisterPage = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password2: '',
  })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (formData.password !== formData.password2) {
      toast.error('Les mots de passe ne correspondent pas')
      return
    }
    
    setLoading(true)
    
    try {
      await dispatch(register(formData)).unwrap()
      toast.success('Inscription réussie! Vous pouvez maintenant vous connecter')
      navigate('/login')
    } catch (error) {
      const errors = error.response?.data
      if (errors?.username) toast.error(errors.username[0])
      else if (errors?.email) toast.error(errors.email[0])
      else if (errors?.password) toast.error(errors.password[0])
      else toast.error('Erreur lors de l\'inscription')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Créer un compte
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Ou{' '}
            <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
              connectez-vous
            </Link>
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <input
                type="text"
                name="first_name"
                placeholder="Prénom"
                value={formData.first_name}
                onChange={handleChange}
                className="input-field"
              />
              <input
                type="text"
                name="last_name"
                placeholder="Nom"
                value={formData.last_name}
                onChange={handleChange}
                className="input-field"
              />
            </div>
            <input
              type="text"
              name="username"
              required
              placeholder="Nom d'utilisateur"
              value={formData.username}
              onChange={handleChange}
              className="input-field"
            />
            <input
              type="email"
              name="email"
              required
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className="input-field"
            />
            <input
              type="password"
              name="password"
              required
              placeholder="Mot de passe"
              value={formData.password}
              onChange={handleChange}
              className="input-field"
            />
            <input
              type="password"
              name="password2"
              required
              placeholder="Confirmer le mot de passe"
              value={formData.password2}
              onChange={handleChange}
              className="input-field"
            />
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full disabled:opacity-50"
            >
              {loading ? 'Inscription...' : "S'inscrire"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default RegisterPage