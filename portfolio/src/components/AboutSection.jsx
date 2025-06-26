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
                <p>Hey it's me Edgardo, I'm a pretty chill guy who doesn't sweat the small stuff. I love jumping into new projects, whether by myself or with others, usually figuring things out as I go. When I find some free time, I enjoy coding random little things, mostly fun stuff for me or my friends. I got into visual design through making memes, which eventually led to helping non-profits and designing my own project websites.</p>
                <p>Travel is another passion, the real backpacking kind, far from five-star hotels. I'm just back from an 8-month trip through Latin America, hitting 14 countries with almost no flights involved. Oh, also I really like cooking too, mainly because, well, I really like eating.
            </p>
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
