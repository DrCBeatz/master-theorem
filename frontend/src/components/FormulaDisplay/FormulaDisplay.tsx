// src/components/FormulaDisplay/FormulaDisplay.tsx
import React from 'react';

interface FormulaDisplayProps {
  a: string;
  b: string;
  k: string;
}

const FormulaDisplay: React.FC<FormulaDisplayProps> = ({ a, b, k }) => {
  return (
    <div className="formula-container">
      <strong className="formula-text">
        T(n) ={' '}
        <span className={`variable-default ${a ? 'variable-a' : ''}`}>
          {a || 'a'}
        </span>
        T(n/
        <span className={`variable-default ${b ? 'variable-b' : ''}`}>
          {b || 'b'}
        </span>
        ) + f(n
        <sup>
          <span className={`variable-default ${k ? 'variable-k' : ''}`}>
            {k || 'k'}
          </span>
        </sup>
        )
      </strong>
    </div>
  );
};

export default FormulaDisplay;
