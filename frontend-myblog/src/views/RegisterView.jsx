export default function RegisterView() {
  return (
    <>
      <div className="row">
        <div className="col col-md-6 col-xl-6 col-lg-6">
          <div className="d-block register-view">
            <img src="ds.png" className="register-img" alt="Image_register" />
          </div>
          <div className="d-block register-view">
            <fieldset className="form-group">
              <legend className="border-bottom mb-4">Registrarse</legend>
              <form method="post">
                {/*{{form.hidden_tag()}}*/}
                {/*{{form_field(form.username, class = "form-control")}}*/}
                {/*{{form_field(form.email, class = "form-control")}}*/}
                {/*{{form_field(form.password, class = "form-control")}}*/}
                {/*{{form_field(form.password_conf, class = "form-control")}}*/}
                <div className="d-flex justify-content-between justify-intems-center">
                  <a className="text-decoration-none" href="/">
                    <i className="fas fa-sign-in-alt" />
                    Iniciar Sesión
                  </a>
                </div>
              </form>
            </fieldset>
          </div>
        </div>
      </div>
    </>
  );
}
