import React from 'react'
import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white mt-16">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-xl font-bold mb-4">FashionStore</h3>
            <p className="text-gray-400 text-sm">
              Votre destination mode préférée pour les vêtements tendance pour hommes et femmes.
            </p>
          </div>
          
          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Liens rapides</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link to="/shop" className="hover:text-white">Boutique</Link></li>
              <li><Link to="/shop?gender=M" className="hover:text-white">Homme</Link></li>
              <li><Link to="/shop?gender=F" className="hover:text-white">Femme</Link></li>
              <li><Link to="/about" className="hover:text-white">À propos</Link></li>
            </ul>
          </div>
          
          {/* Customer Service */}
          <div>
            <h3 className="font-semibold mb-4">Service client</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link to="/contact" className="hover:text-white">Contact</Link></li>
              <li><Link to="/faq" className="hover:text-white">FAQ</Link></li>
              <li><Link to="/shipping" className="hover:text-white">Livraison</Link></li>
              <li><Link to="/returns" className="hover:text-white">Retours</Link></li>
            </ul>
          </div>
          
          {/* Contact */}
          <div>
            <h3 className="font-semibold mb-4">Contact</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>Email: contact@fashionstore.com</li>
              <li>Tél: +212 5XX XXX XXX</li>
              <li>Lun-Ven: 9h - 18h</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2024 FashionStore. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer