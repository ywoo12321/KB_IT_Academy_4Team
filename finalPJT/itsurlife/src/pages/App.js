import styled from "@emotion/styled";
import theme from "../styles/theme";

const App = () => {
  return (
    <NavBox>
      <p>
        나만의ddd
        <br /> 감성숙소를 찾아주다ㅇㅇ
      </p>
    </NavBox>
  );
};

export default App;

const NavBox = styled.div`
  width: 100%;
  height: 300px;
  background-color: blue;
  & > p {
    color: ${theme.color.whiteFont};
    font-family: ${theme.font_family.T};
    font-size: ${theme.font_size.tittle};
  }
`;
