import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { loadStripe } from '@stripe/stripe-js'
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js'
import toast from 'react-hot-toast'
import api from '../services/api'
import { clearCart } from '../store/slices/cartSlice'

// Initialiser Stripe avec la clé publique
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

const CheckoutForm = () => {
  const stripe = useStripe()
  const elements = useElements()
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const { total_price } = useSelector(state => state.cart)
  const { profile } = useSelector(state => state.auth)
  
  const [formData, setFormData] = useState({
    shipping_address: profile?.address || '',
    shipping_city: profile?.city || '',
    shipping_postal_code: profile?.postal_code || '',
    shipping_country: profile?.country || 'Maroc',
    phone: profile?.phone || '',
    email: profile?.user?.email || '',
    notes: '',
  })
  
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!stripe || !elements) {
      toast.error('Stripe non initialisé')
      return
    }
    
    setLoading(true)
    
    try {
      // 1. Créer l'intention de paiement
      const { data: paymentIntent } = await api.post('/payments/create-payment-intent/', {
        amount: total_price
      })
      
      // 2. Confirmer le paiement avec Stripe
      const cardElement = elements.getElement(CardElement)
      
      const { error: paymentMethodError, paymentMethod } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
      })
      
      if (paymentMethodError) {
        toast.error(paymentMethodError.message)
        setLoading(false)
        return
      }
      
      // 3. Confirmer le paiement
      const { error: confirmError } = await stripe.confirmCardPayment(
        paymentIntent.client_secret,
        {
          payment_method: paymentMethod.id,
        }
      )
      
      if (confirmError) {
        toast.error(confirmError.message)
        setLoading(false)
        return
      }
      
      // 4. Paiement réussi - Créer la commande
      const { data: order } = await api.post('/orders/create/', formData)
      
      dispatch(clearCart())
      toast.success('Paiement réussi ! Commande confirmée')
      navigate(`/orders/${order.id}`)
      
    } catch (error) {
      console.error('Payment error:', error)
      toast.error('Erreur lors du paiement')
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <h3 className="font-semibold mb-3">Informations de livraison</h3>
        <div className="space-y-3">
          <input
            type="text"
            name="shipping_address"
            placeholder="Adresse"
            value={formData.shipping_address}
            onChange={handleChange}
            required
            className="input-field"
          />
          <div className="grid grid-cols-2 gap-3">
            <input
              type="text"
              name="shipping_city"
              placeholder="Ville"
              value={formData.shipping_city}
              onChange={handleChange}
              required
              className="input-field"
            />
            <input
              type="text"
              name="shipping_postal_code"
              placeholder="Code postal"
              value={formData.shipping_postal_code}
              onChange={handleChange}
              required
              className="input-field"
            />
          </div>
          <input
            type="text"
            name="shipping_country"
            placeholder="Pays"
            value={formData.shipping_country}
            onChange={handleChange}
            required
            className="input-field"
          />
          <input
            type="tel"
            name="phone"
            placeholder="Téléphone"
            value={formData.phone}
            onChange={handleChange}
            required
            className="input-field"
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
            className="input-field"
          />
          <textarea
            name="notes"
            placeholder="Notes (optionnel)"
            value={formData.notes}
            onChange={handleChange}
            className="input-field"
            rows="3"
          />
        </div>
      </div>
      
      <div>
        <h3 className="font-semibold mb-3">Informations de paiement</h3>
        <div className="border border-gray-300 rounded-lg p-4">
          <CardElement
            options={{
              style: {
                base: {
                  fontSize: '16px',
                  color: '#424770',
                  '::placeholder': {
                    color: '#aab7c4',
                  },
                },
              },
            }}
          />
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Mode test - Utilisez la carte : 4242 4242 4242 4242
        </p>
      </div>
      
      <button
        type="submit"
        disabled={!stripe || loading}
        className="btn-primary w-full disabled:opacity-50"
      >
        {loading ? 'Traitement en cours...' : `Payer ${total_price} MAD`}
      </button>
    </form>
  )
}

const CheckoutPage = () => {
  const { total_price, items } = useSelector(state => state.cart)
  
  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold mb-4">Votre panier est vide</h2>
        <p className="text-gray-600 mb-8">Ajoutez des produits avant de passer commande</p>
        <Link to="/shop" className="btn-primary inline-block">
          Continuer mes achats
        </Link>
      </div>
    )
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Finaliser la commande</h1>
      
      <div className="flex flex-col lg:flex-row gap-8">
        <div className="lg:w-2/3">
          <div className="bg-white rounded-lg shadow-md p-6">
            <Elements stripe={stripePromise}>
              <CheckoutForm />
            </Elements>
          </div>
        </div>
        
        <div className="lg:w-1/3">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-24">
            <h2 className="text-xl font-bold mb-4">Récapitulatif</h2>
            <div className="space-y-3 max-h-96 overflow-y-auto mb-4">
              {items.map(item => (
                <div key={item.id} className="flex gap-3">
                  <img
                    src={item.product_image || '/images/placeholder.svg'}
                    alt={item.product_name}
                    className="w-16 h-16 object-cover rounded"
                  />
                  <div className="flex-1">
                    <p className="font-semibold text-sm">{item.product_name}</p>
                    <p className="text-xs text-gray-500">Qté: {item.quantity}</p>
                    <p className="text-sm font-medium">{item.total_price} MAD</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="border-t pt-3">
              <div className="flex justify-between font-bold text-lg">
                <span>Total</span>
                <span className="text-indigo-600">{total_price} MAD</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CheckoutPage