// Copyright 2015 Canonical Ltd.
// Licensed under the AGPLv3, see LICENCE file for details.

package unitassigner

import (
	"github.com/juju/juju/api/base"
	"github.com/juju/juju/api/watcher"
	"github.com/juju/juju/apiserver/params"
)

const uaFacade = "UnitAssigner"

// API provides access to the UnitAssigner API facade.
type API struct {
	facade base.FacadeCaller
}

// New creates a new client-side UnitAssigner facade.
func New(caller base.APICaller) API {
	fc := base.NewFacadeCaller(caller, uaFacade)
	return API{facade: fc}
}

// AssignUnits tells the state server to run whatever unit assignments it has.
func (a API) AssignUnits() (params.AssignUnitsResults, error) {
	var result params.AssignUnitsResults
	if err := a.facade.FacadeCall("AssignUnits", nil, &result); err != nil {
		return result, err
	}
	return result, nil
}

// WatchUnitAssignments watches the server for new unit assignments to be
// created.
func (a API) WatchUnitAssignments() (watcher.NotifyWatcher, error) {
	var result params.NotifyWatchResult
	err := a.facade.FacadeCall("WatchUnitAssignments", nil, &result)
	if err != nil {
		return nil, err
	}
	if result.Error != nil {
		return nil, result.Error
	}
	w := watcher.NewNotifyWatcher(a.facade.RawAPICaller(), result)
	return w, nil
}
