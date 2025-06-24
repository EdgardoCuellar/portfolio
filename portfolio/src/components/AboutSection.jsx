import { FaLaptopCode, FaPlane, FaUtensils, FaPenNib } from "react-icons/fa";

export default function AboutSection() {
  return (
    <section
      id="about"
      className="py-16 px-6 bg-accent-secondary text-text flex flex-col md:flex-row items-center justify-center gap-10 max-w-4xl mx-auto rounded-2xl shadow-lg"
    >
      {/* Image (à remplacer par la tienne plus tard) */}
      <div className="w-40 h-40 rounded-full overflow-hidden border-4 border-accent shadow-md">
        {/* Remplace src par ton image plus tard */}
        <img
          src="/placeholder.jpg"
          alt="Edgardo Cuellar Sanchez"
          className="w-full h-full object-cover"
        />
      </div>

      {/* Texte */}
      <div className="text-center md:text-left max-w-md space-y-4">
        <h2 className="text-2xl font-bold text-white">About Me</h2>
        <p className="text-lg leading-relaxed">
          J’adore créer des projets qui allient technique et esthétique.
          Quand je ne code pas, je conçois des affiches ou des interfaces, je pars en sac à dos découvrir de nouveaux horizons,
          ou je prépare à manger avec ce que je trouve sous la main.  
          J’aime apprendre, partager, et rendre les choses un peu plus claires autour de moi.
        </p>

        {/* Petits icônes hobbies */}
        <div className="flex gap-4 text-accent text-xl justify-center md:justify-start pt-2">
          <FaLaptopCode title="Dev" />
          <FaPenNib title="Design" />
          <FaPlane title="Voyages" />
          <FaUtensils title="Cuisine" />
        </div>
      </div>
    </section>
  );
}
