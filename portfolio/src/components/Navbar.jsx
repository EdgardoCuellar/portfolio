// src/components/Navbar.jsx
export default function Navbar({ sections, scrollTo }) {
  return (
    <nav className="w-full py-4 flex justify-center">
      <ul className="flex space-x-6 text-m font-bold">
        {sections.map(({ id, label }) => (
          <li key={id}>
            <button
              onClick={() => scrollTo(id)}
              className="relative text-text transition duration-300 ease-in-out hover:text-accent"
            >
              {label}
              <span className="absolute left-0 bottom-0 w-0 h-0.5 bg-accent transition-all duration-300 ease-in-out group-hover:w-full"></span>
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
