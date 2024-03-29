// frontend/src/components/Header/Header.tsx

import React from "react";
import { MDBCardHeader } from "mdb-react-ui-kit";

interface HeaderProps {
  title: string;
}

const Header: React.FC<HeaderProps> = ({ title }) => {
  return (
    <MDBCardHeader>
      <h1 className="main-header">{title}</h1>
    </MDBCardHeader>
  );
};

export default Header;
