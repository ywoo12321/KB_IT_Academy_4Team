import styled from "@emotion/styled";
import theme from "../styles/theme";
import LandingPage from "./LandingPage";

const App = () => {
  return (
    <>
      <LandingPage />
      <NavBox />
    </>
  );
};

export default App;

const NavBox = styled.div`
  width: 1920px;
  height: 79px;
  background-color: #7097a8;
`;
