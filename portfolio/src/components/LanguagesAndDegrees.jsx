import { FaGraduationCap } from 'react-icons/fa';

export default function LanguagesAndDegrees() {
  const languages = [
    { name: 'French', level: 'C2', color: 'border-accent text-accent' },
    { name: 'Spanish', level: 'C1', color: 'border-red-500 text-red-500' },
    { name: 'English', level: 'C1', color: 'border-yellow-500 text-yellow-500' },
    { name: 'Dutch', level: 'A2', color: 'border-green-500 text-green-500' },
  ];

    const degrees = [
    {
        title: "Master in Computer Science",
        school: "ULB & UQAM",
        honors: "With Highest Distinction",
        year: "2024"
    },
    {
        title: "Bachelor in Computer Science",
        school: "ULB",
        honors: "With Distinction",
        year: "2022"
    }
    ];

  return (
    <section id="languages-degrees" className="py-8 px-6 max-w-5xl mx-auto">
      <div className="grid md:grid-cols-2 gap-12">
        {/* LANGUAGES */}
        <div>
          <h3 className="text-xl font-semibold text-white text-center mb-6">Languages</h3>
          <div className="grid sm:grid-cols-2 gap-4">
            {languages.map(({ name, level, color }) => (
              <div
                key={name}
                className={`p-4 border rounded-xl text-center ${color} font-bold transition hover:scale-105 duration-200`}
              >
                <p className="text-lg">{name}</p>
                <p className="text-sm opacity-75">Level: {level}</p>
              </div>
            ))}
          </div>
        </div>

        {/* DEGREES */}
        <div>
          <h3 className="text-xl font-semibold text-white text-center mb-4">Academic</h3>
            <div className="relative flex flex-col items-center">

                <div className="z-10 mb-2">
                    <FaGraduationCap className="text-accent text-3xl" />
                </div>

                <div className="h-6 w-0.5 bg-accent-secondary" />

                {/* Liste des diplômes avec lignes fines entre eux */}
                <div className="flex flex-col items-center relative">
                {degrees.map((deg, idx) => (
                    <div key={idx} className="relative flex flex-col items-center">
                        {idx !== 0 && (
                        <div className="w-0.5 h-8 bg-accent-secondary" />
                        )}
                        <div className="text-center bg-background px-4 py-2">
                        <p className="text-lg text-text font-semibold">{deg.title}</p>
                        <p className="text-sm text-accent-secondary italic">
                            {deg.school} – {deg.year}
                        </p>
                        <p className="text-sm text-text">{deg.honors}</p>
                        </div>
                    </div>
                ))}

                <div className="w-0.5 h-6 bg-accent-secondary mt-2" />

            </div>
            </div>
        </div>
      </div>
    </section>
  );
}
