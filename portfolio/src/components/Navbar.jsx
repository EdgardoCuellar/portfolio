// src/components/Navbar.jsx
export default function Navbar({ sections, scrollTo }) {
  return (
    <nav className="w-full py-4 flex justify-center sticky top-0 bg-primary z-50">
      <ul className="flex space-x-6 text-m font-bold">
        {sections.map(({ id, label }) => (
          <li key={id}>
            <button
              onClick={() => scrollTo(id)}
              className="relative text-text group transition duration-300 ease-in-out hover:text-accent"
            >
              {label}
              <span className="absolute left-0 bottom-[-2px] h-0.5 bg-accent w-0 transition-all duration-300 ease-in-out group-hover:w-full"></span>
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
