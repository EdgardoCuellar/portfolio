import rentizyImg from "../assets/rentizy.png"
import smalsImg from "../assets/smals.png"

export const projects = [
  {
    title: "Rentizy",
    date: "2024 - 2025",
    description: "A real estate MVP platform built in Django.A real estate MVP platform built in Django.",
    icon: "🌐",
    tools: ["Python", "Django"],
    details: {
      text: "Rentizy is a real estate management tool developed with Django, featuring full CRUD, authentication, and admin features. It was a collaborative project with a small team and included weekly SCRUM meetings.",
      image: rentizyImg,
      link: "https://rentizy.io/"
    }
  },
    {
    title: "ShareHub",
    date: "2023 - 2024",
    description: "A second-hand marketplace platform built in Django.",
    icon: "🌐",
    tools: ["Python", "Django"],
    details: {
      text: "Rentizy is a real estate management tool developed with Django, featuring full CRUD, authentication, and admin features. It was a collaborative project with a small team and included weekly SCRUM meetings.",
      image: null,
      link: null
    }
  },
    {
    title: "ShareHub",
    date: "2023 - 2024",
    description: "A second-hand marketplace platform built in Django.",
    icon: "🌐",
    tools: ["Python", "Django"],
    details: {
      text: "Rentizy is a real estate management tool developed with Django, featuring full CRUD, authentication, and admin features. It was a collaborative project with a small team and included weekly SCRUM meetings.",
      image: null,
      link: null
    }
  },
    {
    title: "ShareHub",
    date: "2023 - 2024",
    description: "A second-hand marketplace platform built in Django.",
    icon: "🌐",
    tools: ["Python", "Django"],
    details: {
      text: "Rentizy is a real estate management tool developed with Django, featuring full CRUD, authentication, and admin features. It was a collaborative project with a small team and included weekly SCRUM meetings.",
      image: null,
      link: null
    }
  },
    {
    title: "ShareHub",
    date: "2023 - 2024",
    description: "A second-hand marketplace platform built in Django.",
    icon: "🌐",
    tools: ["Python", "Django"],
    details: {
      text: "Rentizy is a real estate management tool developed with Django, featuring full CRUD, authentication, and admin features. It was a collaborative project with a small team and included weekly SCRUM meetings.",
      image: null,
      link: null
    }
  },
  // Add more projects here
];

// src/components/Projects.jsx
import { useState } from "react";

export default function ProjectsSection() {
  const [selected, setSelected] = useState(null);

  return (
    <section id="projects" className="py-8 px-6 max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold text-center text-text mb-12">Projects</h2>
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((proj, idx) => (
          <div
            key={idx}
            className="bg-secondary p-6 rounded-lg shadow-md relative cursor-pointer border border-transparent hover:border-accent hover:shadow-lg transition duration-300"
            onClick={() => setSelected(proj)}
          >
            <div className="flex items-center gap-2 mb-4">
              <span className="w-3 h-3 rounded-full bg-red-500"></span>
              <span className="w-3 h-3 rounded-full bg-yellow-400"></span>
              <span className="w-3 h-3 rounded-full bg-green-500"></span>
            </div>
            <div className="absolute top-2 right-2 text-xl">{proj.icon}</div>
            <h3 className="text-xl font-semibold text-text">{proj.title}</h3>
            <p className="text-sm text-accent-secondary">{proj.date}</p>
            <p className="text-sm mt-2 text-text">{proj.description}</p>
            <p className="text-xs mt-3 text-accent">{proj.tools?.join(", ")}</p>
          </div>
        ))}
      </div>

      {selected && (
        <div
          className="fixed inset-0 backdrop-blur-sm flex items-center justify-center z-50"
          onClick={() => setSelected(null)}
        >
          <div
            className="bg-secondary p-8 rounded-lg max-w-xl w-[90%] relative shadow-lg"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="absolute top-2 right-2 text-gray-500 hover:text-red-500"
              onClick={() => setSelected(null)}
            >
              ✖
            </button>
            {selected.details.image && (
              <img src={selected.details.image} alt={selected.title} className="mb-4 rounded" />
            )}
            <h3 className="text-2xl font-bold text-text mb-2">{selected.title}</h3>
            <p className="text-sm text-accent-secondary mb-4">{selected.date}</p>
            {selected.tools && (
                <p className="text-xs text-accent mb-4">{selected.tools.join(", ")}</p>
            )}
            <p className="text-text text-justify">{selected.details.text}</p>
            {selected.details.link && (
              <a
                href={selected.details.link}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-block text-accent hover:underline"
              >
                Visit project ↗
              </a>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
