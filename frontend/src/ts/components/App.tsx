import React, { useEffect } from "react";
import { connect } from "react-redux";

import { Header } from "./Header";
import { Map } from "./Map";
import { Visualisation } from "./Visualisation";
import { Spinner } from "./Spinner";
import { IState } from "../reducers";
import { Dispatch } from "redux";
import { getOverviewData } from "../actions/xhr";

interface IAppStateProps {
  isLoading: boolean;
}

interface IAppDispatchProps {
  getOverviewData: () => void;
}

interface IAppProps extends IAppStateProps, IAppDispatchProps {}

const AppComponent = ({ isLoading, getOverviewData }: IAppProps) => {
  useEffect(() => {
    getOverviewData();
  }, [getOverviewData]);

  return (
    <div className="App">
      {isLoading && <Spinner />}
      <Header />
      <Map />
      <Visualisation />
    </div>
  );
};

const mapStateToProps = (state: IState): IAppStateProps => {
  const { isLoading } = state.loading;
  return { isLoading };
};

const mapDispatchToProps = (dispatch: Dispatch): IAppDispatchProps => {
  return {
    getOverviewData: () => {
      getOverviewData()(dispatch);
    },
  };
};

const App = connect(mapStateToProps, mapDispatchToProps)(AppComponent);

export default App;
