const metrics = {
  throughput: { weight: 0.3 },
  reliability: { weight: 0.3 },
  quality: { weight: 0.25 },
  responsiveness: { weight: 0.15 }
};

const gradeBoundaries = [
  { min: 90, grade: 'A', message: 'Excellent operations health.' },
  { min: 80, grade: 'B', message: 'Strong, with minor opportunities to improve.' },
  { min: 70, grade: 'C', message: 'Stable baseline, improvement recommended.' },
  { min: 60, grade: 'D', message: 'At risk. Prioritize reliability and quality fixes.' },
  { min: 0, grade: 'F', message: 'Critical condition. Immediate intervention needed.' }
];

function getGrade(score) {
  return gradeBoundaries.find((entry) => score >= entry.min);
}

function calculateScore() {
  let score = 0;

  Object.entries(metrics).forEach(([id, config]) => {
    const input = document.getElementById(id);
    const output = document.getElementById(`${id}Value`);
    const value = Number(input.value);
    output.textContent = value;
    score += value * config.weight;
  });

  const rounded = Math.round(score);
  const graded = getGrade(rounded);

  document.getElementById('score').textContent = String(rounded);
  document.getElementById('grade').textContent = graded.grade;
  document.getElementById('status').textContent = graded.message;
}

Object.keys(metrics).forEach((id) => {
  document.getElementById(id).addEventListener('input', calculateScore);
});

calculateScore();
