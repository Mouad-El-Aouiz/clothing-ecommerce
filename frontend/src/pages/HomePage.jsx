import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import ProductCard from '../components/products/ProductCard'
import { fetchFeatured, fetchNewArrivals, fetchCategories, fetchProducts } from '../store/slices/productSlice'

const HomePage = () => {
  const dispatch = useDispatch()
  const { featured, newArrivals, categories } = useSelector(state => state.products)
  const [currentHeroIndex, setCurrentHeroIndex] = useState(0)
  const [heroImages, setHeroImages] = useState([])
  const [popularCategories, setPopularCategories] = useState([])

  useEffect(() => {
    dispatch(fetchFeatured())
    dispatch(fetchNewArrivals())
    dispatch(fetchCategories())
  }, [dispatch])

  // Construire les images hero et catégories UNIQUEMENT avec les images de la BDD
  useEffect(() => {
    if (categories && categories.length > 0) {
      // 🔧 RECHERCHE PAR ID (plus fiable que par nom)
      const menCategory = categories.find(cat => cat.id === 48)  // Vêtements Homme
      const womenCategory = categories.find(cat => cat.id === 2)  // Vêtements Femme
      const accessoriesCategory = categories.find(cat => cat.id === 3)  // ACCESSOIRES
      const sportCategory = categories.find(cat => cat.id === 4)  // Sport & Loisirs

      console.log('👨 Catégorie Homme (ID 48):', menCategory?.name, 'Image:', !!menCategory?.image)
      console.log('👩 Catégorie Femme (ID 2):', womenCategory?.name, 'Image:', !!womenCategory?.image)
      console.log('👜 Accessoires (ID 3):', accessoriesCategory?.name, 'Image:', !!accessoriesCategory?.image)
      console.log('⚽ Sport (ID 4):', sportCategory?.name, 'Image:', !!sportCategory?.image)

      // 1. Récupérer les images des catégories pour le carrousel
      const newHeroImages = []
      
      if (menCategory?.image) {
        newHeroImages.push({
          src: menCategory.image,
          alt: 'Collection Homme',
          link: '/shop/homme',
          title: 'Collection Homme',
          subtitle: 'Tendances automne/hiver 2024'
        })
      }
      
      if (womenCategory?.image) {
        newHeroImages.push({
          src: womenCategory.image,
          alt: 'Collection Femme',
          link: '/shop/femme',
          title: 'Collection Femme',
          subtitle: 'Élégance et confort au quotidien'
        })
      }
      
      if (accessoriesCategory?.image) {
        newHeroImages.push({
          src: accessoriesCategory.image,
          alt: 'Accessoires',
          link: '/shop',
          title: 'Accessoires',
          subtitle: 'Le détail qui fait la différence'
        })
      }
      
      if (sportCategory?.image) {
        newHeroImages.push({
          src: sportCategory.image,
          alt: 'Sport & Loisirs',
          link: '/shop',
          title: 'Sport & Loisirs',
          subtitle: 'Performance et style'
        })
      }
      
      console.log('🎠 Images hero construites:', newHeroImages.length)
      setHeroImages(newHeroImages)

      // 2. Récupérer les images pour les catégories populaires
      const newPopularCategories = []
      
      if (menCategory?.image) {
        newPopularCategories.push({
          name: 'Vêtements Homme',
          link: '/shop/homme',
          image: menCategory.image,
          color: 'from-indigo-900/80'
        })
      }
      
      if (womenCategory?.image) {
        newPopularCategories.push({
          name: 'Vêtements Femme',
          link: '/shop/femme',
          image: womenCategory.image,
          color: 'from-pink-900/80'
        })
      }
      
      setPopularCategories(newPopularCategories)
    }
  }, [categories])

  // Rotation du carrousel
  useEffect(() => {
    if (heroImages.length <= 1) return
    const interval = setInterval(() => {
      setCurrentHeroIndex((prev) => (prev + 1) % heroImages.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [heroImages.length])

  // Si pas d'images, ne rien afficher
  if (heroImages.length === 0) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement des images...</p>
        </div>
      </div>
    )
  }

  const currentHero = heroImages[currentHeroIndex]

  const fadeUp = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0 }
  }

  const staggerContainer = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  }

  return (
    <div className="overflow-x-hidden">
      
      {/* ==================== HERO SECTION (CARROUSEL) ==================== */}
      <section className="relative h-screen min-h-[600px] max-h-[900px] overflow-hidden">
        <div className="absolute inset-0">
          <img
            src={currentHero.src}
            alt={currentHero.alt}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-black/60 via-black/30 to-transparent" />
        </div>

        {/* Indicateurs de slide */}
        <div className="absolute bottom-8 left-0 right-0 z-20 flex justify-center gap-3">
          {heroImages.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentHeroIndex(index)}
              className={`transition-all duration-300 rounded-full ${
                index === currentHeroIndex 
                  ? 'w-10 h-1 bg-white' 
                  : 'w-4 h-1 bg-white/40 hover:bg-white/60'
              }`}
            />
          ))}
        </div>

        {/* Contenu Hero */}
        <div className="relative z-10 h-full flex items-center">
          <div className="container mx-auto px-4 md:px-8">
            <motion.div
              key={currentHeroIndex}
              initial="hidden"
              animate="visible"
              variants={fadeUp}
              transition={{ duration: 0.6 }}
              className="max-w-2xl text-white"
            >
              <span className="inline-block text-sm uppercase tracking-wider mb-4 border-l-3 border-white pl-3">
                Nouvelle saison
              </span>
              <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
                {currentHero.title}
              </h1>
              <p className="text-lg md:text-xl text-white/90 mb-8 leading-relaxed">
                {currentHero.subtitle}
              </p>
              <Link
                to={currentHero.link}
                className="inline-flex items-center gap-2 bg-white text-gray-900 px-8 py-3 rounded-full font-medium hover:bg-gray-100 transition-all duration-300 group"
              >
                Explorer maintenant
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ==================== CATÉGORIES POPULAIRES ==================== */}
      {popularCategories.length > 0 && (
        <section className="py-20 px-4 bg-white">
          <div className="container mx-auto max-w-6xl">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, amount: 0.3 }}
              variants={fadeUp}
              transition={{ duration: 0.5 }}
              className="text-center mb-12"
            >
              <span className="text-indigo-600 text-sm uppercase tracking-wider font-semibold">Nos collections</span>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mt-2">Découvrez nos univers</h2>
              <div className="w-20 h-1 bg-indigo-600 mx-auto mt-4 rounded-full" />
            </motion.div>

            <motion.div
              variants={staggerContainer}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, amount: 0.3 }}
              className="grid grid-cols-1 md:grid-cols-2 gap-8"
            >
              {popularCategories.map((category, index) => (
                <motion.div
                  key={category.name}
                  variants={fadeUp}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500"
                >
                  <Link to={category.link}>
                    <div className="relative h-96 overflow-hidden">
                      <img
                        src={category.image}
                        alt={category.name}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
                      />
                      <div className={`absolute inset-0 bg-gradient-to-t ${category.color} to-transparent opacity-70 group-hover:opacity-80 transition-opacity duration-300`} />
                      <div className="absolute bottom-0 left-0 right-0 p-8 text-white">
                        <h3 className="text-2xl md:text-3xl font-bold mb-2">{category.name}</h3>
                        <span className="inline-flex items-center gap-1 text-sm font-medium group-hover:gap-2 transition-all">
                          Découvrir
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                          </svg>
                        </span>
                      </div>
                    </div>
                  </Link>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>
      )}

      {/* ==================== PRODUITS VEDETTES ==================== */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="container mx-auto max-w-7xl">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.3 }}
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="text-center mb-12"
          >
            <span className="text-indigo-600 text-sm uppercase tracking-wider font-semibold">Sélection</span>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mt-2">Produits vedettes</h2>
            <p className="text-gray-500 mt-3 max-w-2xl mx-auto">Les articles les plus populaires de la saison</p>
            <div className="w-20 h-1 bg-indigo-600 mx-auto mt-4 rounded-full" />
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {featured.slice(0, 4).map((product, index) => (
              <motion.div
                key={product.id}
                variants={fadeUp}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <ProductCard product={product} />
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>
     
      {/* ==================== NOUVEAUTÉS ==================== */}
      <section className="py-20 px-4 bg-white">
        <div className="container mx-auto max-w-7xl">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.3 }}
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="text-center mb-12"
          >
            <span className="text-indigo-600 text-sm uppercase tracking-wider font-semibold">Juste arrivé</span>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mt-2">Nouveautés</h2>
            <p className="text-gray-500 mt-3 max-w-2xl mx-auto">Les dernières tendances à découvrir</p>
            <div className="w-20 h-1 bg-indigo-600 mx-auto mt-4 rounded-full" />
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {newArrivals.slice(0, 4).map((product, index) => (
              <motion.div
                key={product.id}
                variants={fadeUp}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <ProductCard product={product} />
              </motion.div>
            ))}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="text-center mt-12"
          >
            <Link to="/shop" className="inline-flex items-center gap-2 px-8 py-3 border-2 border-gray-300 rounded-full text-gray-700 font-medium hover:border-indigo-600 hover:text-indigo-600 transition-all duration-300">
              Découvrir toute la collection
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default HomePage