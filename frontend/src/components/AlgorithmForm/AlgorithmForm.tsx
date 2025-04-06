// frontend/src/components/AlgorithmForm/AlgorithmForm.tsx

import React, { useState, useEffect } from "react";
import { MDBInput, MDBSelect, MDBBtn } from "mdb-react-ui-kit";
import { SelectData } from "mdb-react-ui-kit/dist/types/pro/forms/SelectV2/types";

import { getAlgorithms } from "../../services/apiService";

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
  onSubmit: (
    a: string,
    b: string,
    k: string,
    selectedAlgorithm?: AlgorithmType
  ) => void;
  onUpdateA: (a: string) => void;
  onUpdateB: (b: string) => void;
  onUpdateK: (k: string) => void;
}

const AlgorithmForm: React.FC<AlgorithmFormProps> = ({
  onSubmit,
  onUpdateA,
  onUpdateB,
  onUpdateK,
}) => {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [k, setK] = useState("");
  const [algorithms, setAlgorithms] = useState<AlgorithmType[]>([]);
  const [inputsDisabled, setInputsDisabled] = useState(false);
  const [selectedAlgorithmId, setSelectedAlgorithmId] = useState<number | null>(
    null
  );
  useState<AlgorithmType | null>(null);

  useEffect(() => {
    const fetchAlgorithms = async () => {
      try {
        // Use service function
        const data = await getAlgorithms();
        setAlgorithms(data);
      } catch (error) {
        console.error("Failed to fetch algorithms:", error);
      }
    };
    fetchAlgorithms();
  }, []);

  const handleIntegerInputChange = (
    value: string,
    setter: React.Dispatch<React.SetStateAction<string>>,
    updateCallback: (value: string) => void
  ) => {
    if (/^\d*$/.test(value)) {
      setter(value);
      updateCallback(value);
    }
  };

  const handleAlgorithmChange = (data: SelectData | SelectData[]) => {
    const value = Array.isArray(data) ? data[0]?.value : data.value;

    if (typeof value === "string") {
      const algorithmId = parseInt(value, 10);

      if (algorithmId === -1) {
        setInputsDisabled(false);
        setA("");
        setB("");
        setK("");
        onUpdateA("");
        onUpdateB("");
        onUpdateK("");

        setSelectedAlgorithmId(null);
      } else {
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
          setSelectedAlgorithmId(algorithmId);
        } else {
          // This case shouldn't occur since "Enter Values" and valid algorithm IDs are handled above
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
    const selectedAlgorithm = algorithms.find(
      (alg) => alg.id === selectedAlgorithmId
    );
    onSubmit(a, b, k, selectedAlgorithm);
  };

  const selectOptions = [
    { text: "Enter Values", value: "-1" },
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
        label="b (factor to reduce problem size)"
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
        label="k (non-recursive work exponent)"
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
          label="Enter Values or Choose Algorithm"
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
