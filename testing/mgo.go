// Copyright 2012, 2013 Canonical Ltd.
// Licensed under the AGPLv3, see LICENCE file for details.

package testing

import (
	"os"
	"testing"

	gitjujutesting "github.com/juju/testing"
)

// MgoTestPackage should be called to register the tests for any package
// that requires a connection to a MongoDB server.
//
// The server will be configured without SSL enabled, which slows down
// tests. For tests that care about security (which should be few), use
// MgoSSLTestPackage.
func MgoTestPackage(t *testing.T) {
	var disable = os.Getenv("DISABLE_MONGO_TESTS") == "yes"

	if disable {
		t.Skip("Asked to disable mongo tests via $DISABLE_MONGO_TESTS environment variable")
		return
	}

	gitjujutesting.MgoTestPackage(t, nil)
}

// MgoSSLTestPackage should be called to register the tests for any package
// that requires a secure (SSL) connection to a MongoDB server.
func MgoSSLTestPackage(t *testing.T) {
	gitjujutesting.MgoTestPackage(t, Certs)
}
