import styled from "@emotion/styled";
import theme from "../styles/theme";
import Randing1 from "../images/Landing1.png";

const LandingPage = () => {
  return (
    <FirstBox>
      <BigImageBox>
        <img src={Randing1} width="864" height="1080" alt="Landing1" />
      </BigImageBox>
      <FirstRightBox>
        <FirstTextBox>
          <p>
            나만의
            <br /> 감성숙소를 찾아주다
          </p>
        </FirstTextBox>
        <GoToMainBtn>
          <div className="first">
            <p>둘러보기</p>
          </div>
        </GoToMainBtn>
      </FirstRightBox>
    </FirstBox>
  );
};

export default LandingPage;

const FirstBox = styled.div`
  width: 1920px;
  height: 1080px;
  display: block;
  display: flex;
  flex-direction: column;
  flex-direction: row;
  justify-content: space-between;
`;
const BigImageBox = styled.div`
  width: 864px;
  height: 100vh;
`;
const FirstRightBox = styled.div`
  display: flex;
  flex-direction: column;
`;
const FirstTextBox = styled.div`
  width: 800px;
  height: 280px;
  margin-top: 654px;
  margin-right: 76px;
  text-align: right;
  & > p {
    font-family: ${theme.font_family.T};
    font-size: ${theme.font_size.tittle};
  }
`;
const GoToMainBtn = styled.div`
  & > .first {
    margin-top: 20px;
    margin-bottom: 158px;
    margin-right: 76px;
    text-align: right;
    & > p {
      font-family: ${theme.font_family.N};
      font-size: ${theme.font_size.h2};
      color: ${theme.color.main};
      opacity: 0.8;
    }
  }
`;
