// src/components/ResultDisplay/ResultDisplay.tsx
import React, { useEffect, useRef } from "react";
import Chart from "chart.js/auto";
import {
  MDBCard,
  MDBCardBody,
  MDBCardHeader,
  MDBCardText,
  MDBAccordion,
  MDBAccordionItem,
  MDBIcon,
} from "mdb-react-ui-kit";
import { ResultType, AlgorithmType } from "../../App";

const CASE_3 = "Case 3: Θ(n<sup>k</sup>)"; // Define or import this constant

interface ResultDisplayProps {
  result: ResultType;
  selectedAlgorithmDetails: AlgorithmType | null;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({
  result,
  selectedAlgorithmDetails,
}) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstanceRef = useRef<Chart | null>(null); // To hold the chart instance

  useEffect(() => {
    if (result?.plot_data && chartRef.current) {
      const ctx = chartRef.current.getContext("2d");
      if (ctx) {
        // Destroy previous chart instance if it exists
        if (chartInstanceRef.current) {
          chartInstanceRef.current.destroy();
        }
        // Create new chart instance
        chartInstanceRef.current = new Chart(ctx, {
          type: "line",
          data: {
            labels: result.plot_data.n,
            datasets: [
              {
                label: "n^log_b(a)",
                data: result.plot_data.n_log_b_a,
                borderColor: "blue",
                borderWidth: 1,
                fill: false,
              },
              {
                label: "f(n)",
                data: result.plot_data.f_n,
                borderColor: "red",
                borderWidth: 2,
                fill: false,
                borderDash: [5, 5],
              },
              {
                label: "Time Complexity",
                data: result.plot_data.time_complexity,
                borderColor: "green",
                borderWidth: 2,
                fill: false,
                borderDash: [10, 5],
              },
            ],
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: "Function Value", // Y-axis label
                  color: "#888",
                  font: {
                    size: 12,
                  },
                },
                ticks: {},
              },
              x: {
                grid: {
                  display: true,
                },
                ticks: {
                  callback: function (value) {
                    return Number(value).toFixed(0); // Rounds the value to the nearest whole number
                  },
                },
                title: {
                  display: true,
                  text: "Input Size (n)", // X-axis label
                  color: "#888",
                  font: {
                    size: 12,
                  },
                },
              },
            },
            plugins: {
              legend: {
                display: true,
                position: "top", // Position of the legend
                labels: {
                  boxWidth: 20, // Width of the legend color box
                  padding: 10, // Padding between legend items
                },
              },
              tooltip: {
                enabled: true,
              },
            },
            elements: {
              line: {
                borderWidth: 1, // Set line thickness
              },
              point: {
                radius: 0, // Hide points on the line
              },
            },
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      }
    }

    // Cleanup function to destroy chart on component unmount or before re-render
    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
        chartInstanceRef.current = null;
      }
    };
  }, [result]); // Dependency array includes result

  return (
    <MDBCard className="my-4">
      <MDBCardHeader>
        <h2>Evaluation</h2>
      </MDBCardHeader>
      <MDBCardBody className="evaluation-card-body">
        {/* Ensure canvas has a unique ID or use the ref */}
        <canvas
          ref={chartRef}
          id="evaluationChart"
          className="mb-3"
          style={{ minHeight: "300px" }}
        ></canvas>

        <MDBCardText>
          <strong>Recurrence Relation: </strong>
          <span
            dangerouslySetInnerHTML={{ __html: result.recurrence_relation }}
          ></span>
        </MDBCardText>
        <MDBCardText data-testid="evaluation-case">
          <strong>Evaluation: </strong>
          <span dangerouslySetInnerHTML={{ __html: result.case }}></span>
        </MDBCardText>

        {result.case.includes(CASE_3) && (
          <MDBCardText>
            <strong>Regularity Condition Met:</strong>{" "}
            {result.regularity_condition_met !== undefined &&
              (result.regularity_condition_met ? "Yes" : "No")}
          </MDBCardText>
        )}

        <MDBCardText>
          <strong>Time Complexity: </strong>
          <span dangerouslySetInnerHTML={{ __html: result.complexity }}></span>
        </MDBCardText>
      </MDBCardBody>

      {selectedAlgorithmDetails && (
        <>
          <h4>{selectedAlgorithmDetails.name} Algorithm</h4>
          <MDBAccordion alwaysOpen initialActive={1}>
            <MDBAccordionItem
              className="left-align"
              collapseId={1} // Use unique numbers or strings
              headerTitle={
                <>
                  <MDBIcon fas icon="question-circle" /> Algorithm Description
                </>
              }
            >
              <article>{selectedAlgorithmDetails.description}</article>
            </MDBAccordionItem>
            <MDBAccordionItem
              className="left-align" // Added left-align class here too
              collapseId={2} // Use unique numbers or strings
              headerTitle={
                <>
                  <MDBIcon fab icon="python" /> Python Code
                </>
              }
            >
              <pre className="left-align">
                <code>{selectedAlgorithmDetails.python_code}</code>
              </pre>
            </MDBAccordionItem>
          </MDBAccordion>
        </>
      )}
    </MDBCard>
  );
};

export default ResultDisplay;
