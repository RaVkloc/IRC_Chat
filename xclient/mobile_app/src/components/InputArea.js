import React from 'react';
import {StyleSheet, TextInput} from 'react-native';

class InputArea extends React.Component {
  render() {
    return (
      <TextInput
        selectionColor={'#428AF8'}
        style={[styles.textInput, this.props.style]}
        {...this.props}
      />
    );
  }
}

const styles = StyleSheet.create({
  textInput: {
    height: 40,
    borderColor: '#BEBEBE',
    borderBottomWidth: StyleSheet.hairlineWidth,
    marginBottom: 20,
  },
});

export default InputArea;
