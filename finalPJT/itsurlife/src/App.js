import styled from "@emotion/styled";

const App = () => {
  return (
    <NavBox>
      <p>ddd</p>
    </NavBox>
  );
};

export default App;

const NavBox = styled.div`
  width: 100%;
  height: 60px;
  background-color: blue;
  & > p {
    color: #ffffff;
  }
`;
