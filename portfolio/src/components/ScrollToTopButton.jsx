// src/components/ScrollToTopButton.jsx
export default function ScrollToTopButton({ scrollTo }) {
  return (
    <button
      className="fixed bottom-4 right-4 bg-gray-800 text-white p-2 rounded-full shadow-lg hover:bg-gray-700 transition"
      onClick={() => scrollTo('intro')}
    >
      ↑
    </button>
  );
}
