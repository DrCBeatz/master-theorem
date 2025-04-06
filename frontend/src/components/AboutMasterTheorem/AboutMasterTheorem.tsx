// src/components/AboutMasterTheorem/AboutMasterTheorem.tsx
import React from "react";
import {
  MDBCard,
  MDBCardHeader,
  MDBAccordion,
  MDBAccordionItem,
} from "mdb-react-ui-kit";

const AboutMasterTheorem: React.FC = () => {
  return (
    <MDBCard alignment="center" className="my-4">
      <MDBCardHeader>
        <h2>About the Master Theorem</h2>
      </MDBCardHeader>
      <MDBAccordion initialActive={1}>
        <MDBAccordionItem
          className="left-align"
          collapseId={1}
          headerTitle="What is the Master Theorem?"
        >
          <article>
            <p>
              The <strong>Master Theorem</strong> offers a straightforward way
              to determine the time complexity of recursive algorithms,
              especially those that follow the divide and conquer approach. This
              theorem simplifies the process of analyzing how efficiently an
              algorithm runs as the size of its input increases. It is
              particularly useful for computer scientists and software engineers
              to predict algorithm performance without the need for detailed
              benchmarks.
            </p>
            <p>
              The following parameters are required to evaluate an algorithm
              using the Master Theorem:
            </p>
            <ul>
              <li>
                <strong>a</strong> = the number of recursive subproblems.
              </li>
              <li>
                <strong>b</strong> = the factor by which the problem size is
                reduced.
              </li>
              <li>
                <strong>k</strong> = the exponent in the work done outside of
                the recursive function.
              </li>
            </ul>
          </article>
        </MDBAccordionItem>
        <MDBAccordionItem
          className="left-align"
          collapseId={2}
          headerTitle="Decoding the Master Recurrence"
        >
          <article>
            <p>
              The Master Theorem can only be used to evaluate recursive
              algorithms with the following recurrence relation:
            </p>
            <p className="text-center">
              <strong>T(n) = aT(n/b) + f(n)</strong>
            </p>
            <p>
              This equation is the heart of the Master Theorem. and is called
              the <strong>Master Recurrence</strong>. It captures the essence of
              divide and conquer algorithms:
            </p>
            <ul>
              <li>
                <strong>T(n)</strong> is the total time complexity we aim to
                find.
              </li>
              <li>
                <strong>aT(n/b)</strong> represents the time taken by the
                recursive subproblems.
              </li>
              <li>
                <strong>f(n)</strong> is the time taken by the work done outside
                the recursive calls, such as dividing the problem or combining
                the results.
              </li>
            </ul>
            <p>
              Evaluating the Master Theorem involves comparing the rate of
              growth of two separate functions:
            </p>
            <ul>
              <p className="text-center">
                <strong>
                  n<sup>logb(a)</sup> + f(n)
                </strong>
              </p>

              <li>
                <strong>
                  n
                  <sup>
                    log<sub>b</sub>(a)
                  </sup>
                </strong>{" "}
                is also known as the <strong>watershed function.</strong>
              </li>
              <li>
                <strong>f(n)</strong> is also known as the{" "}
                <strong>driving function.</strong>
              </li>
            </ul>
            <p>
              Comparing the growth rate of these 2 functions results in either
              of 3 possible cases.
            </p>
          </article>
        </MDBAccordionItem>
        <MDBAccordionItem
          className="left-align"
          collapseId={3}
          headerTitle="The 3 Cases of the Master Theorem"
        >
          <article>
            <p>
              <strong>Case 1</strong>: n
              <sup>
                log<sub>b</sub>(a)
              </sup>{" "}
              grows asymptotically and polynomially greater than f(n):
            </p>
            <p className="text-center">
              <strong>
                T(n) = n
                <sup>
                  log<sub>b</sub>(a)
                </sup>
              </strong>
            </p>

            <p>
              <strong>Case 2:</strong> n
              <sup>
                log<sub>b</sub>(a)
              </sup>{" "}
              and f(n) grow at the same rate:
            </p>
            <p className="text-center">
              <strong>
                T(n) = n<sup>k</sup> log(n)
              </strong>
            </p>

            <p>
              <strong>Case 3:</strong> f(n) grows assymptotically and
              polynomially greater than n
              <sup>
                log<sub>b</sub>(a)
              </sup>{" "}
              (and must also fulfill the{" "}
              <strong>
                regularity condition
                <sup>*</sup>)
              </strong>{" "}
              :
            </p>
            <p className="text-center">
              <strong>
                T(n) = f(n<sup>k</sup>)
              </strong>
            </p>
            <ul>
              <li>
                <strong>Case 1</strong> occurs when the split subproblems
                dominate the overall time complexity. It implies that as we
                break the problem down, the sheer number of subproblems is the
                primary driver of the complexity.
              </li>
              <li>
                <strong>Case 2</strong> occurs when the work done at each level
                of recursion is just as significant as the number of
                subproblems. This balance means the time complexity is a
                combination of the dividing/conquering work and the depth of the
                recursion.
              </li>
              <li>
                <strong>Case 3</strong> highlights scenarios where the work done
                outside the recursive calls (combining solutions, for instance)
                is the main factor determining the time complexity. This is
                typically seen in algorithms where merging or processing results
                is more intensive than breaking down the problem.
              </li>
            </ul>
            <p>
              <small>
                <strong>* </strong>
                The regularity condition ensures that the work done at the
                recursive levels does not grow too quickly compared to the work
                done to divide the problem and combine the results. This
                condition helps maintain the integrity of the complexity
                analysis provided by the theorem.
              </small>
            </p>
          </article>
        </MDBAccordionItem>
      </MDBAccordion>
    </MDBCard>
  );
};

export default AboutMasterTheorem;
