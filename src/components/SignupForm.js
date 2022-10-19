import Btn from "./Btn";
import styled from "@emotion/styled";
import theme from "../styles/theme";

const SignupForm = () => {
  return (
    <Form className="login">
      <Title>당신에 대하여 알려주세요</Title>
      <div>
        <span>ID</span>
        <input type="text" name="id" />
      </div>
      <div>
        <span>ID</span>
        <input type="text" name="id" />
      </div>
      <div>
        <span>ID</span>
        <input type="text" name="id" />
      </div>
      <div>
        <span>ID</span>
        <input type="text" name="id" />
      </div>
      <div>
        <span>PW</span>
        <input type="password" name="pw" />
      </div>
      <div className="btncontainer">
        <Btn>홈으로</Btn>
        <Btn>로그인</Btn>
      </div>
    </Form>
  );
};

export default SignupForm;

const Form = styled.form`
  background-color: ${theme.color.point};
  border-radius: 40px;
  text-align: center;
  width: 1280px;
  margin: 175px auto 175px auto;

  & {
    height: 570px;
  }

  & > div {
    text-align: center;
  }
  & > div > span {
    display: inline-block;
    text-align: center;
    width: 65px;
    font-size: ${theme.font_size.h2};
    margin-right: 14px;
  }

  & > div > input {
    border-radius: 30px;
    border: none;
    height: 55px;
    margin-bottom: 58px;
    padding-left: 20px;
    font-size: ${theme.font_size.subtitle1};
    font-family: ${theme.font_family.T};
  }

  & > div > input[name="id"] {
    width: 500px;
  }

  & > div > input[name="pw"] {
    width: 500px;
  }

  & > .btncontainer > button {
    margin: 30px 75px 20px 75px;
  }
`;

const Title = styled.h1`
  display: inline-block;
  margin-top: 30px;
  margin-bottom: 75px;
  font-family: ${theme.font_family.T};
  font-size: ${theme.font_size.h1};
  margin-left: auto;
  margin-right: auto;
`;
