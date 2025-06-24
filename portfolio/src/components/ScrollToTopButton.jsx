import { HiChevronUp } from 'react-icons/hi';

export default function ScrollToTopButton({ scrollTo }) {
  return (
    <button
      onClick={() => scrollTo('intro')}
      className="fixed bottom-6 right-6 p-3 rounded-full bg-accent-secondary text-text shadow-lg hover:bg-accent transition duration-300 z-50"
      aria-label="Scroll to top"
    >
      <HiChevronUp className="w-6 h-6" />
    </button>
  );
}
