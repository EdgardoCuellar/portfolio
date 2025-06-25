import { FaLaptopCode, FaUtensils } from "react-icons/fa";
import { LuBackpack } from "react-icons/lu"
import { MdOutlineDraw } from "react-icons/md";
import imgOfMe from "../assets/moi_lama.png";

export default function AboutSection() {
  return (
    <section id="about" className="py-10 px-6 max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold text-center text-text mb-10">About Me</h2>
      <div className="flex flex-col md:flex-row items-center gap-10">
        {/* Image style flat design */}
        <div className="w-full md:w-1/3 flex justify-center">
          <div className="rounded-xl overflow-hidden shadow-md border border-accent-secondary bg-background">
            <img
              src={imgOfMe}
              alt="Edgardo Cuellar Sanchez"
              className="w-full h-full object-cover"
            />
          </div>
        </div>

        {/* Text section */}
        <div className="w-full md:w-2/3 text-text space-y-4">
          <p className="leading-relaxed">
            Passionate about building smart digital solutions, creating clean and useful visual interfaces,
            and discovering the world one meal and one hike at a time. I enjoy crafting things that are both
            functional and beautiful — whether it's a line of code, a poster, or a good recipe.
          </p>
          <div className="flex flex-wrap gap-4 pt-2">
            <span className="flex items-center gap-2 text-sm font-semibold text-accent">
              <FaLaptopCode /> IT Projects
            </span>
            <span className="flex items-center gap-2 text-sm font-semibold text-accent">
              <LuBackpack /> Backpacking
            </span>
            <span className="flex items-center gap-2 text-sm font-semibold text-accent">
              <MdOutlineDraw /> Design
            </span>
            <span className="flex items-center gap-2 text-sm font-semibold text-accent">
              <FaUtensils /> Cooking
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
