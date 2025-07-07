const skills = [
    { name: "Java", type: "programming" },
    { name: "C", type: "programming" },
    { name: "C++", type: "programming" },
    { name: "Python", type: "programming" },
    { name: "JavaScript", type: "programming" },
    { name: "ASML", type: "programming" },
    { name: "HTML", type: "programming" },
    { name: "PHP", type: "programming" },
    { name: "SQL", type: "database" },
    { name: "PostgreSQL", type: "database" },
    { name: "Spark", type: "database" },
    { name: "Pytorch", type: "ia" },
    { name: "Django", type: "framework" },
    { name: "React", type: "framework" },
    { name: "Flutter", type: "framework" },
    { name: "Node.js", type: "framework" },
    { name: "Agile", type: "methodology" },
    { name: "Scrum", type: "methodology" },
    { name: "UML", type: "methodology" },
    { name: "CSS", type: "design" },
    { name: "TailwindCSS", type: "design" },
    { name: "Figma", type: "design" },
    { name: "Photoshop", type: "design" },
    { name: "Ilustrator", type: "design" },
    { name: "GitHub", type: "programming" },
    { name: "Docker", type: "programming" },
    { name: "Linux", type: "programming" },
    { name: "Bash", type: "programming" },
];

const typeColors = {
    programming: "border-blue-500 text-blue-500",
    framework: "border-green-500 text-green-500",
    methodology: "border-purple-500 text-purple-500",
    design: "border-pink-500 text-pink-500",
    database: "border-yellow-500 text-yellow-500",
    ia: "border-red-500 text-red-500",
};

export default function Skills() {
  return (
    <section id="skills" className="py-8 px-6 max-w-6xl mx-auto mt-4">
      <h2 className="text-3xl font-bold text-center text-text mb-12">Skills</h2>
      <div className="flex flex-wrap gap-3 justify-center">
        {skills.map((skill, idx) => (
          <span
            key={idx}
            className={`px-4 py-2 rounded-full border-2 font-bold transition duration-200 hover:scale-105 ${typeColors[skill.type]}`}
          >
            {skill.name}
          </span>
        ))}
      </div>
    </section>
  );
}