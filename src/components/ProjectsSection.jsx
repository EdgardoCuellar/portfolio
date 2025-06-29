import rentizyImg from "../assets/rentizy.png"
import autochefImg from "../assets/autochef.png"
import bubbleImg from "../assets/bubble_game.png"
import chatedImg from "../assets/chated.png"
import esnImg from "../assets/esn.jpg"
import lopsaImg from "../assets/lopsa.png"
import ltypeImg from "../assets/ltype.png"
import sharehubImg from "../assets/sharehub.png"
import stickmanImg from "../assets/stickman_basement.png"

export const projects = [
  {
    title: "Rentizy",
    date: "2023 - 2025",
    description: "A platform simplifying property rental and management for both landlords and tenants",
    icon: "🏠",
    tools: ["Django", "TailwindCSS", "JavaScript", "SQL", "Azure", "Agile", "UML"],
    details: {
      text: `\
Rentizy is a property management MVP designed to simplify and automate the rental process for both property owners and tenants. From auto-generating rental contracts to handling maintenance reports and enabling property search for individuals and co-living arrangements, the platform centralizes everything.
I co-founded the project with a partner who brought the initial idea and business expertise. I led the technical development using Django, TailwindCSS, JavaScript, SQL, and Azure, while we worked in agile methodology and with some UML schema with regular short call meetings. Later, we expanded the team to four by hiring a UI/UX designer and a backend developer.
The project ran from November 2023 to January 2025, when I quit to focus on my long backpack trip.`,
      image: rentizyImg,
      link: "https://rentizy.io/"
    }
  },
    {
    title: "ShareHub",
    date: "2023 - 2024",
    description: "A second-hand syllabus marketplace built from scratch with a redistributive model",
    icon: "🌐",
    tools: ["Django", "TailwindCSS", "JavaScript", "SQL", "Docker", "Nginx", "Apache", "Photoshop"],
    details: {
      text: `\
ShareHub is a full-featured second-hand marketplace I built alone during my master's thesis. The platform focuses on reselling university course materials with a redistributive economic model.
I handled the entire development cycle, from backend logic with Django to frontend interfaces using TailwindCSS and JavaScript, plus deployment on Linux servers with Docker, Nginx, and Apache. I included some features like encrypted messaging, account management, rating systems, and filtered searches.
All UI/UX design was done by me, primarily using Photoshop. I also managed outreach and promotional efforts through social media and university networks.`,
      image: sharehubImg,
      link: "https://github.com/EdgardoCuellar/ShareHub"
    }
  },
    {
    title: "Communcation manager ESN ULB Brussels",
    date: "2023 - 2024",
    description: "Lead communications for an international student organization with 4K+ followers.",
    icon: "🖼️",
    tools: ["Photoshop", "Illustrator", "Canva", "Social Media", "Project Management"],
    details: {
      text: `\
Between December 2023 and December 2024, I was Communication Manager for ESN ULB Brussels, a student association organizing weekly events for international students and young professionals.
I managed our Instagram account (then ~3500 followers), produced visual assets (posters, stories, stickers), and coordinated communication campaigns using tools like Photoshop, Canva, and Illustrator.
I also led a team expansion by recruiting two collaborators halfway through, helping us and improve efficiency. This experience gave me hands-on exposure to team management, project coordination, conflict resolution, and event promotion, with our team of 14 core members and 60 volunteers.`,
      image: esnImg,
      link: "https://www.instagram.com/esnulbbrussels/"
    }
  },
    {
    title: "Shark Classifier & Generative AI",
    date: "2023",
    description: "An image classification and generation model for aquatic animals and candy",
    icon: "🎮",
    tools: ["PyTorch", "CNN", "ImageNet", "Generative Models"],
    details: {
      text: `This short project involved classifying images of sharks, dolphins, and whales using a convolutional neural network built with PyTorch. Once we removed the final classification layer, we repurposed the model into a generative network capable of producing realistic shark images from noise.
We trained it on an open-source animal dataset (ImageNet) before training a similar network to classify different Haribo candy types because why not?
The project was a fun and creative dive into LLM, transfer learning and generative networks.`,
      image: null,
      link: "https://github.com/EdgardoCuellar/autoencodeur_animaux_marins"
    }
  },
    {
    title: "Anime recommender",
    date: "2023",
    description: "A big data project using PySpark to recommend anime with hybrid recommendation using PySpark",
    icon: "🤓",
    tools: ["Apache Spark", "Big Data", "Recommender Systems", "Python", "PySpark"],
    details: {
      text: `An anime recommendation system built using Big Data tools, notably Apache Spark. We implemented a hybrid recommendation model combining collaborative filtering (based on user preferences) with content-based filtering (based on anime features like genre, rating, etc).
The system handled large datasets efficiently and provided personalized suggestions while maintaining scalability. We fine-tuned the performance using Spark’s and integrated it into a clean frontend demo to show the results.
This project taught us a lot about recommender systems, big data pipelines, and model evaluation in distributed environments.`,
      image: null,
      link: "https://github.com/EdgardoCuellar/Anime-recommandation"
    }
  },
    {
    title: "My own programming language",
    date: "2023",
    description: "A custom-made, minimal programming language written in Python.",
    icon: "🧠",
    tools: ["Python", "Compilers", "Interpreter", "Parsing"],
    details: {
      text: `A minimalist programming language I co-developed with a friend over two months, as part of a university course on programming languages. It supported arithmetic operations, loops, conditionals, and jumps.
The project aimed to help us deeply understand parsing, evaluation, and compiler theory. We wrote a full interpreter from scratch in Python, simulating a low-level execution model.
Designing and debugging a language from the ground up was one of the most mentally challenging and rewarding experiences I've had in code.`,
      image: null,
      link: "https://github.com/EdgardoCuellar/FortressLanguage"
    }
  },
    {
    title: "MNIST Number Recognizer",
    date: "2022",
    description: "A basic handwritten digit recognizer using a multilayer neural network",
    icon: "🔢",
    tools: ["LLM", "CUDA", "MNIST", "Neural Network"],
    details: {
      text: `In this project, we implemented and explained a simple neural network capable of recognizing handwritten digits from the MNIST dataset. Built with a multi-layer perceptron and trained on an NVIDIA GPU using CUDA, the core of the model (as we joked) was basically just a fancy pile of matrix multiplications.
One of our teammates even created a short video to explain the project in an accessible way, it made for a nice mix of machine learning and science communication.`,
      image: null,
      link: "https://www.youtube.com/watch?v=vvz41yM6C48"
    }
  },
    {
    title: "AutoChef",
    date: "2021 - 2022",
    description: "A collaborative Java project managing recipes, menus, and groceries in a simulated company",
    icon: "🧑‍🍳",
    tools: ["Java", "SCRUM", "UML", "OOP", "Open Source"],
    details: {
      text: `\
AutoChef is a desktop application built in Java by a team of 9, simulating a real company environment to manage recipes, menus, and grocery planning. The project was designed to teach team collaboration, documentation (SRD), and agile methods with a dedicated SCRUM master.
In reality, three of us carried most of the development, and I personally took on the leadership and core logic development, especially the recipe, menu, and calendar features. With Java’s strong object-oriented model, this project was a deep dive into software architecture.
It has it's intense work phases, sometimes exceeding 40 hours a week to hit our delivery goals. We were proud of the final result, which we published open source, and were awarded the highest grade out of 11 teams.`,
      image: autochefImg,
      link: "https://github.com/etoome/AutoChef"
    }
  },
    {
    title: "Lopsa",
    date: "2021",
    description: "A party game mobile app for drinking nights, made in Flutter",
    icon: "📱",
    tools: ["Flutter", "Dart", "State Management"],
    details: {
      text: `Lopsa is a drinking game mobile app developed with Flutter. It was my second attempt at mobile development and a major improvement over my Java-based app experience.
Flutter’s reactive approach and state management made building the UI much smoother. I learned a lot about managing game states and UI logic in a more structured way.
Fun fact: the app was eventually banned from the Play Store, but I still have the source code and a working version on my phone, used occasionally at parties.`,
      image: lopsaImg,
      link: null
    }
  },
    {
    title: "L-Type",
    date: "2020 - 2021",
    description: "An online C++ shoot-em-up game with a custom OpenGL engine.",
    icon: "🎮",
    tools: ["C++", "OpenGL", "GitHub", "UML", "CI/CD"],
    details: {
      text: `\
L-Type is an online shoot-em-up video game developed over one year as a university team project. Our team of 8 was effectively 3 developers, with myself managing the creation of a custom OpenGL engine that enabled easier development for the rest of the group.
I also designed and coded the entire menu system. The project emphasized object-oriented programming, teamwork, server logic, delivery deadlines, quality assurance, and continuous integration via GitHub workflows. We earned the highest grade in the entire class.`,  
      image: ltypeImg,
      link: "https://github.com/ULB-INFO-F-209/l-type-groupe-2-2020"
    }
  },
    {
    title: "PHP Social Network",
    date: "2018 - 2019",
    description: "A complete social network clone built from scratch in raw PHP HTML CSS and SQL",
    icon: "🌐",
    tools: ["PHP", "SQL", "HTML", "CSS", "JavaScript"],
    details: {
      text: `This was my first real web project, a complete social network made entirely in PHP, HTML, CSS, SQL, and just a little JavaScript. It was inspired by platforms like Facebook, and included user profiles, posts, likes, and more.
Though the code was a bit chaotic in retrospect, it taught me how to build a website from scratch and introduced me to full-stack web development. I was young and learning fast, so no judgment please!
There’s still a demo video online showing what I built.`,
      image: chatedImg,
      link: "https://www.youtube.com/watch?v=Ugi7VaJtZJ8"
    }
  },
    {
    title: "Reflexed",
    date: "2018",
    description: "A second-hand marketplace platform built in Django.",
    icon: "📱",
    tools: ["Java", "Android Studio"],
    details: {
      text: `Reflexed was my first mobile app, developed in Java using Android Studio. The goal was to challenge reflexes and mental math speed through quick interactions and timers.
It was created after I followed a few tutorials, then expanded it on my own. As my first step into Android development, it taught me about app structure, UI basics, and event handling.
Sadly, like many early projects, I lost the code and APK. Still, it marks a significant milestone in my developer journey.`,
      image: null,
      link: null
    }
  },
    {
    title: "Bubbled (Game prototype)",
    date: "2017",
    description: "A polished arcade game built in Construct 2 almost without writing code",
    icon: "🎮",
    tools: ["Construct 2", "Game Design", "No-Code"],
    details: {
      text: `Space Defender is a complete arcade-style game I created using Construct 2, a no-code game engine that relies on visual logic and JavaScript-style event systems.
I was quite proud of this one, not only because I learned to master a new tool, but because I created an original and fun concept that felt complete. This was during the time I wanted to work in the game industry.
Thankfully, I didn’t lose the files, and I still have a video from that time showcasing the gameplay.`,
      image: bubbleImg,
      link: "https://youtu.be/_IDuZsoMH7Y"
    }
  },
    {
    title: "Stickman Basement",
    date: "2017",
    description: "My first big project: a Python gravity platformer made with Pygame",
    icon: "🎮",
    tools: ["Python", "Pygame", "Game Engine"],
    details: {
      text: `Stickman Basement was the first serious project I ever developed, a 2D gravity-based platformer built with Python and Pygame over three months of coding.
It was rough and experimental, but it helped me create my first mini game engine and understand object oriented programming. That early experience laid the foundation for the game engine I later wrote for L-Type.
Unfortunately, I lost all the original files, and only a short video remains, a nostalgic relic of my beginnings in code.`,
      image: stickmanImg,
      link: "https://youtu.be/zm79zrDI1Z0"
    }
  },
  {
  title: "Others",
  description: "Collection of small and personal creative experiments.",
  tools: ["Python", "JavaScript", "C", "React", "AI", "Fun"],
  icon: "✨",
  date: "2015 – 2025",
  isOthers: true,
  details: {
    text: `A bunch of small personal or experimental projects I've built along the way:

- An AI chatbot using ChatGPT fine tuned to mimic my friends messages.
- A fractal explorer to zoom deep into fractals sets.
- Pathfinding algorithms for maze solving and shortest path demo.
- A simplified real-time simulation of the solar system.
- An image matching algorithm to stitch photos into a big panorama.
- An implementation of Conway’s Game of Life.
- And many more unfinished prototypes, weekend hacks, or curiosities...

Sometimes the smallest projects are the most fun.`,
  }
}

];

import { useState } from "react";

export default function ProjectsSection() {
  const [selected, setSelected] = useState(null);
  const isOthers = (proj) => proj.isOthers;
  return (
    <section id="projects" className="py-8 px-6 max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold text-center text-text mb-12">Projects</h2>
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((proj, idx) => (
          <div
            key={idx}
            className={`relative p-6 rounded-lg cursor-pointer border transition duration-300 ${
              proj.isOthers
                ? "bg-transparent border-accent border-dashed text-accent-secondary shadow-none hover:shadow-md hover:bg-secondary/10 hover:border-accent-secondary"
                : "bg-secondary border-transparent hover:border-accent hover:shadow-lg shadow-md text-text"
            }`}
            onClick={() => setSelected(proj)}
          >
            {!proj.isOthers && (
              <div className="flex items-center gap-2 mb-4">
                <span className="w-3 h-3 rounded-full bg-red-500"></span>
                <span className="w-3 h-3 rounded-full bg-yellow-400"></span>
                <span className="w-3 h-3 rounded-full bg-green-500"></span>
              </div>
            )}

            <div className="absolute top-2 right-2 text-xl">
              {typeof proj.icon === "string" ? proj.icon : <proj.icon />}
            </div>

            <h3 className="text-xl font-semibold">{proj.title}</h3>
            <p className="text-sm text-accent-secondary">{proj.date}</p>
            <p className="text-sm mt-2">{proj.description}</p>
            <p className="text-xs mt-3 text-accent">{proj.tools?.join(", ")}</p>
          </div>
        ))}
      </div>

{selected && (
  <div
    className="fixed inset-0 backdrop-blur-sm bg-black/40 flex items-center justify-center z-50 transition-all duration-300 scale-100 hover:scale-[1.02]"
    onClick={() => setSelected(null)}
  >
    <div
      className="bg-secondary rounded-lg max-w-xl w-[90%] shadow-lg overflow-hidden"
      onClick={(e) => e.stopPropagation()}
    >
      <div className="relative max-h-[80vh] overflow-y-auto p-6 pt-10 scrollbar scrollbar-thumb-accent-secondary scrollbar-track-transparent">
        {/* ✅ Petite croix, couleur du thème, mieux placée */}
        <button
          className="absolute top-3 left-3 text-accent-secondary hover:text-accent text-base"
          onClick={() => setSelected(null)}
        >
          ✖
        </button>

        {selected.details.image && (
          <img
            src={selected.details.image}
            alt={selected.title}
            className="mb-4 rounded max-h-64 w-full object-contain"
          />
        )}

        <h3 className="text-2xl font-bold text-text mb-1">{selected.title}</h3>
        <p className="text-sm text-accent-secondary mb-2">{selected.date}</p>
        {selected.tools && (
          <p className="text-xs text-accent mb-4">{selected.tools.join(", ")}</p>
        )}
        <p className="text-text text-justify whitespace-pre-line">
          {selected.details.text}
        </p>

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
  </div>
)}
    </section>
  );
}
