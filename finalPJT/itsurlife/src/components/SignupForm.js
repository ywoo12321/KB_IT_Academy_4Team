import Btn from "./Btn";
import styled from "@emotion/styled";
import theme from "../styles/theme";
import Signupimg from "../images/Signupimg.png";

const SignupForm = () => {
  return (
    <>
      <ImgBox>
        <img src={Signupimg} alt="." />
      </ImgBox>
      <FormBox>
        <Form className="login">
          <Title>당신에 대하여 알려주세요</Title>
          <div>
            <p>ID</p>
            <input
              type="text"
              name="id"
              placeholder="영어와 숫자를 이용하여 3~6자로 생성해주세요"
            />
            <Btn className="checkBtn">중복 확인</Btn>
          </div>
          <div>
            <p>PW</p>
            <input
              type="password"
              name="pw"
              placeholder="영어와 숫자와 특수문자를 이용하여 6~18자로 생성해주세요."
            />
          </div>
          <div>
            <p>PW 확인</p>
            <input
              type="password"
              name="checkpw"
              placeholder="위에서 작성한 pw를 다시 한 번 작성해주세요."
            />
          </div>
          <div>
            <p>닉네임</p>
            <input type="text" name="nickname" placeholder="사용하실 닉네임을 작성해주세요." />
          </div>
          <div>
            <p>거주지역</p>
            <input type="text" name="area" />
          </div>
          <div className="btncontainer">
            <Btn>이전</Btn>
            <Btn>다음</Btn>
          </div>
        </Form>
      </FormBox>
    </>
  );
};

export default SignupForm;

const ImgBox = styled.div`
  display: block;
  width: 35%;
  height: 1000px;
  background: red;
  float: left;

  & > img {
    object-fit: cover;
    width: 100%;
    height: 100%;
  }
`;

const FormBox = styled.div`
  display: block;
  width: 65%;
  height: 1000px;
  float: right;
`;

const Form = styled.form`
  display: block;
  background-color: ${theme.color.whiteFont};
  text-align: center;
  margin: 123px 130px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 40px 40px 40px 46px;

  & {
    height: 745px;
  }

  & > div {
    text-align: start;
  }
  & > div > button {
    margin-left: 20px;
  }
  & > div > p {
    display: inline-block;
    text-align: end;
    padding-right: 13px;
    width: 150px;
    font-size: ${theme.font_size.h3};
    font-family: ${theme.font_family.N};
    margin-right: 14px;
    margin-left: 40px;
  }

  & > div > input {
    width: 500px;
    border-radius: 30px;
    border: none;
    height: 55px;
    margin-bottom: 40px;
    padding-left: 20px;
    outline: none;
    font-size: ${theme.font_size.subtitle1};
    font-family: ${theme.font_family.T};
    background: #f6f5f1;
    border: 1px solid ${theme.color.logoColor};
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);

    ::placeholder {
      font-family: ${theme.font_family.N};
      font-size: 16px;
    }
  }
  & > div > input[name="pw"] {
    width: 683px;
  }

  & > .btncontainer {
    text-align: center;
  }

  & > .btncontainer > button {
    margin: 10px 75px 20px 75px;
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
