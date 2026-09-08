import { createI18n } from 'vue-i18n'
import es from './es'
import en from './en'

const savedLocale = localStorage.getItem('app-locale')

export default createI18n({
  legacy: false,
  locale: savedLocale === 'en' ? 'en' : 'es',
  fallbackLocale: 'es',
  messages: { es, en },
})
