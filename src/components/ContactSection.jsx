export default function ContactSection() {
  return (
    <section id="contact" className="py-8 mb-8 px-6 max-w-3xl mx-auto text-center">
      <h2 className="text-3xl font-bold text-text mb-8">Contact</h2>
      <p className="text-text mb-6">
        Want to get in touch? Whether it's about an opportunity or just to share something cool:
      </p>
      <a
        href="mailto:edgardo-cuellar@hotmail.com"
        target="_blank"
        rel="noopener noreferrer"
        className="relative px-6 py-2 border-2 border-accent-secondary text-accent-secondary font-semibold rounded overflow-hidden group transition-colors duration-300
          shadow-[0_0_8px_1px_theme(colors.accentSecondary/0.5)] animate-pulse"
      >
        <span className="absolute inset-0 left-0 w-0 bg-accent-secondary transition-all duration-300 group-hover:w-full z-0"></span>
        <span className="relative text-lg z-10 group-hover:text-white transition-colors duration-300">
          Email me
        </span>
      </a>
    </section>
  );
}