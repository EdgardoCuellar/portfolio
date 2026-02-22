// src/App.jsx
import { useEffect, useState } from 'react';
import './index.css';
import Navbar from './components/Navbar';
import ScrollToTopButton from './components/ScrollToTopButton';
import IntroSection from './components/IntroSection';
import ProjectsSection from './components/ProjectsSection';
import AboutSection from './components/AboutSection';
import ContactSection from './components/ContactSection';
import Footer from './components/Footer';
import Skills from './components/Skills';
import LanguagesAndDegrees from './components/LanguagesAndDegrees';
import StarsBackground from './components/StarsBackground';

import JobFairWidget from './components/jobfair_widget.jsx';

const sections = [
  { id: 'projects', label: 'Projects' },
  { id: 'skills', label: 'Skills' },
  { id: 'about', label: 'About Me' },
  { id: 'contact', label: 'Contact' },
];

export default function App() {
  const [active, setActive] = useState('intro');
  const [showScrollTop, setShowScrollTop] = useState(false);

  const scrollTo = (id) => {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    setActive(id);
  };

  useEffect(() => {
    const handleScroll = () => {
      const y = window.scrollY;
      setShowScrollTop(y > 200);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="font-sans text-text bg-primary">
      
      <StarsBackground />

      <header className="w-full top-0 left-0 z-10">
        <Navbar sections={sections} scrollTo={scrollTo} />
      </header>


      {showScrollTop && <ScrollToTopButton scrollTo={scrollTo} />}

      <main className="max-w-5xl mx-auto px-4">

        <IntroSection />
        {/* Vite exposes only variables prefixed with VITE_ in import.meta.env */}
        <JobFairWidget apiKey={import.meta.env.VITE_OPEROUTER_API_KEY} /> 
        <ProjectsSection />
        <Skills />
        <LanguagesAndDegrees />
        <AboutSection />
        <ContactSection />
      </main>

      <Footer />
    </div>
  );
}
