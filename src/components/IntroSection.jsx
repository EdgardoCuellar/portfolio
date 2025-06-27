
import { useEffect, useState } from "react";
import { FaGithub, FaLinkedin, FaChevronDown } from "react-icons/fa";

const roles = [
  "Software Engineer",
  "Backend Developer",
  "Functional Analyst",
  "Data Scientist",
];

export default function IntroSection() {
  const [index, setIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const currentRole = roles[index % roles.length];
    let timeout;

    if (isDeleting) {
      timeout = setTimeout(() => {
        setDisplayedText(currentRole.substring(0, displayedText.length - 1));
        if (displayedText === "") {
          setIsDeleting(false);
          setIndex((prev) => prev + 1);
        }
      }, 50);
    } else {
      timeout = setTimeout(() => {
        setDisplayedText(currentRole.substring(0, displayedText.length + 1));
        if (displayedText === currentRole) {
          setTimeout(() => setIsDeleting(true), 1000);
        }
      }, 100);
    }

    return () => clearTimeout(timeout);
  }, [displayedText, isDeleting, index]);

  return (
    <section id="intro" className="h-screen flex flex-col items-center justify-center text-center px-4 -mt-16">
      <h1 className="text-4xl md:text-6xl font-bold text-text">
        Hello, I'm <span className="text-accent">Edgardo</span>
      </h1>
      <h2 className="text-2xl md:text-4xl font-semibold text-text mt-4 h-10">
        A <span className="text-accent-secondary">{displayedText}</span>
      </h2>
      <p className="text-gray-300 md:text-lg text-text max-w-2xl mt-8 text-center">
        Just finished my Master's in Computer Science at ULB with high honors.
        Been coding since I was 14, built all kinds of random stuff along the way. Here's some of my work, and a bit about me too :)
      </p>

    <div className="flex items-center gap-4 mt-8">
      <a
        href="https://github.com/EdgardoCuellar"
        target="_blank"
        rel="noopener noreferrer"
        className="text-accent text-2xl hover:scale-110 transition-transform duration-200"
        aria-label="GitHub"
      >
        <FaGithub />
      </a>
      <a
        href="/portfolio/CV_2025_EN_Edgardo_Cuellar.pdf"
        target="_blank"
        rel="noopener noreferrer"
        className="relative px-6 py-2 border-2 border-accent text-accent font-semibold rounded overflow-hidden group transition-colors duration-300"
      >
        <span className="absolute inset-0 left-0 w-0 bg-accent transition-all duration-300 group-hover:w-full z-0"></span>
        <span className="relative z-10 group-hover:text-white transition-colors duration-300">Resume</span>
      </a>
      <a
        href="https://www.linkedin.com/in/edgardo-cuellar-sanchez/"
        target="_blank"
        rel="noopener noreferrer"
        className="text-accent text-2xl hover:scale-110 transition-transform duration-200"
        aria-label="LinkedIn"
      >
        <FaLinkedin />
      </a>
    </div>
    <div className="absolute bottom-6 left-1/2 -translate-x-1/2 text-accent animate-bounce">
      <FaChevronDown size={28} />
    </div>
    </section>
  );
}
