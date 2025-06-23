
import { useEffect, useState } from "react";

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
      <p className="text-gray-300 md:text-lg text-text max-w-2xl mt-8 text-justify">
        Graduated in Computer Science from ULB with high honors, I’ve been passionate about programming since
I was 14. I worked on many personal projects, including Rentizy, a real estate management MVP developed
with three teammates. After my master’s, I spent eight months traveling across Latin America while still
contributing to the project. I decided to leave it in January to fully enjoy the rest of my trip.
      </p>
    </section>
  );
}
