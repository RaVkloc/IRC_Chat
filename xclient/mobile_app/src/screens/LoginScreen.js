import React from 'react';
import {Image, StyleSheet, View, KeyboardAvoidingView} from 'react-native';
import logo from '../assets/images/logo2.jpg';
import {Button, InputArea} from '../components';

class LoginScreen extends React.Component {
  state = {
    email: '',
    password: '',
  };

  handleEmailChange = email => {
    this.setState({email: email});
  };

  handlePasswordChange = password => {
    this.setState({password: password});
  };

  handleLoginPress = () => {
    console.log('Login button pressed');
    this.props.navigation.navigate('Rooms');
  };

  render() {
    return (
      <KeyboardAvoidingView style={styles.container}>
        <Image source={logo} style={styles.logo} />
        <View style={styles.form}>
          <InputArea
            value={this.state.email}
            onChangeText={this.handleEmailChange}
            placeholder={'e-mail'}
          />
          <InputArea
            value={this.state.password}
            onChangeText={this.handlePasswordChange}
            placeholder={'password'}
          />

          <Button label={'Login'} onPress={this.handleLoginPress} />
        </View>
      </KeyboardAvoidingView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
    alignItems: 'center',
    justifyContent: 'space-between',
    // paddingBottom: 10,
  },
  logo: {
    flex: 1,
    width: '100%',
    resizeMode: 'contain',
    alignSelf: 'center',
  },
  form: {
    marginTop: 20,
    flex: 1,
    justifyContent: 'center',
    width: '80%',
  },
});

export default LoginScreen;
