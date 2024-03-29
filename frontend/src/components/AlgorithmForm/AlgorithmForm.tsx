// frontend/src/components/AlgorithmForm/AlgorithmForm.tsx

import React, { useState, useEffect } from "react";
import { MDBInput, MDBSelect, MDBBtn } from "mdb-react-ui-kit";
import { SelectData } from "mdb-react-ui-kit/dist/types/pro/forms/SelectV2/types";

interface AlgorithmType {
  id: number;
  name: string;
  a: number;
  b: number;
  k: number;
  description: string;
  python_code: string;
}

interface AlgorithmFormProps {
  onSubmit: (a: string, b: string, k: string) => void;
  onAlgorithmSelect: (algorithm: AlgorithmType | null) => void;
  onUpdateA: (a: string) => void;
  onUpdateB: (b: string) => void;
  onUpdateK: (k: string) => void;
}

const AlgorithmForm: React.FC<AlgorithmFormProps> = ({
  onSubmit,
  onAlgorithmSelect,
  onUpdateA,
  onUpdateB,
  onUpdateK,
}) => {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [k, setK] = useState("");
  const [algorithms, setAlgorithms] = useState<AlgorithmType[]>([]);
  const [inputsDisabled, setInputsDisabled] = useState(false);
  useState<AlgorithmType | null>(null);

  useEffect(() => {
    const fetchAlgorithms = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/algorithms`
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setAlgorithms(data); // Store fetched algorithms
      } catch (error) {
        console.error("Failed to fetch algorithms:", error);
      }
    };
    fetchAlgorithms();
  }, []);

  const handleIntegerInputChange = (
    value: string,
    setter: React.Dispatch<React.SetStateAction<string>>,
    updateCallback: (value: string) => void // Add this parameter to receive the corresponding update callback
  ) => {
    if (/^\d*$/.test(value)) {
      setter(value);
      updateCallback(value); // Call the update callback with the new value
    }
  };

  const handleAlgorithmChange = (data: SelectData | SelectData[]) => {
    const value = Array.isArray(data) ? data[0]?.value : data.value;

    if (typeof value === "string") {
      const algorithmId = parseInt(value, 10);

      // Check if the "User Input" option was selected
      if (algorithmId === -1) {
        setInputsDisabled(false); // Enable the inputs
        setA("");
        setB("");
        setK("");
        onUpdateA("");
        onUpdateB("");
        onUpdateK("");

        onAlgorithmSelect?.(null);
      } else {
        // Proceed with finding and setting the selected algorithm
        const selectedAlg =
          algorithms.find((alg) => alg.id === algorithmId) || null;

        if (selectedAlg) {
          setA(selectedAlg.a.toString());
          setB(selectedAlg.b.toString());
          setK(selectedAlg.k.toString());
          onUpdateA(selectedAlg.a.toString());
          onUpdateB(selectedAlg.b.toString());
          onUpdateK(selectedAlg.k.toString());
          setInputsDisabled(true); // Disable the inputs if an algorithm is selected
          onAlgorithmSelect(selectedAlg);
        } else {
          // This case shouldn't occur since "User Input" and valid algorithm IDs are handled above
          console.error("Invalid algorithm selected");
        }
      }
    } else {
      // Handle cases where value is undefined or not a string
      console.error("Selected value is undefined or not a string");
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(a, b, k);
  };

  const selectOptions = [
    { text: "User Input", value: "-1" },
    ...algorithms.map((algorithm) => ({
      text: algorithm.name,
      value: algorithm.id.toString(),
    })),
  ];

  return (
    <form onSubmit={handleSubmit}>
      <MDBInput
        label="a (number of subproblems)"
        id="aInput"
        type="text"
        min="1"
        className="my-4"
        value={a}
        onChange={(e) =>
          handleIntegerInputChange(e.target.value, setA, onUpdateA)
        }
        disabled={inputsDisabled}
      />
      <MDBInput
        label="b (factor by which problem size is reduced)"
        id="bInput"
        type="text"
        min="2"
        className="my-4"
        value={b}
        onChange={(e) =>
          handleIntegerInputChange(e.target.value, setB, onUpdateB)
        }
        disabled={inputsDisabled}
      />
      <MDBInput
        label="k (exponent in the work outside of recursive calls)"
        id="kInput"
        type="text"
        min="0"
        className="my-4"
        value={k}
        onChange={(e) =>
          handleIntegerInputChange(e.target.value, setK, onUpdateK)
        }
        disabled={inputsDisabled}
      />
      <div className="my-4">
        <MDBSelect
          data-testid="algorithm-select"
          data={selectOptions}
          label="Choose Algorithm or Enter Values"
          onChange={handleAlgorithmChange}
        />
      </div>

      <MDBBtn
        type="submit"
        onClick={handleSubmit}
        className="btn-block"
        disabled={!a || !b || !k}
      >
        Evaluate
      </MDBBtn>
    </form>
  );
};

export default AlgorithmForm;
